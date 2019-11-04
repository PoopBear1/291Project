from flask import Flask, escape, request, redirect, send_file, jsonify, make_response, session, abort, send_from_directory
from flask.views import MethodView
import sqlite3
import sys
from flask_cors import CORS

app = Flask(__name__,static_folder='frontend/dist/static', static_url_path='/static')
CORS(app,supports_credentials =True)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "super secret key"

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def connect_db():
    conn = sqlite3.connect(app.config["DB_PATH"])
    conn.row_factory = dict_factory
    return conn

def getUser():
    return {
        "name"  : session.get("fname") + " " + session.get("lname"),
        "type" : session.get("utype")
    }

@app.route("/api/",methods=["GET"])
def init():
    if session:
        return jsonify(getUser())
    return jsonify(0)

@app.route("/api/logout",methods=["GET"])
def logout():
    session.clear()
    return jsonify(1)

@app.route("/api/login",methods=["POST"])
def login():
    form = request.json
    query = '''
        SELECT 
            uid,fname,lname,utype
        FROM 
            users  u
        where upper(uid) = upper(?) and pwd = ?
    '''
    with connect_db() as conn:
        c = conn.cursor()
        c.execute(query, (form.get("uid"),form.get("pwd")))
        row = c.fetchone()
        if row:
            for field in ["uid","fname","lname","utype"]:
                session[field] = row[field]
            return jsonify(getUser())
        else:
            return jsonify(0)

@app.route("/api/register_birth",methods=["post"])
def register_birth():
    if not session:
        abort(400)
    form = request.json    
    query = '''
        select fname,lname
        from persons p
        where upper(fname)=upper(?) and upper(lname) = upper(?)
    '''
    with connect_db() as conn:
        # check if child exist
        c = conn.cursor()
        child = form.get("child")
        if not child:
            abort(400)
        c.execute(query, (child.get("fname"),child.get("lname")))
        row = c.fetchone()
        if row:
            return jsonify({"error" : "Child already exists"})

        more_info_required = []
        parents = {}
        for ptype in ["father","mother"]:
            parent = form.get(ptype)
            c.execute(query,(parent.get("fname"),parent.get("lname")))
            row = c.fetchone()
            if row:
                parents[ptype] = parent
            elif parent.get("more_info"):
                add_person(c,parent)
                parents[ptype] = parent
            else:
                more_info_required.append(ptype)      
        if more_info_required:
            return jsonify({"more_info_required" : more_info_required})

        father = parents["father"]
        mother = parents["mother"]

        query = '''
        insert into births
        select 
            max(regno)+1, 
            ? as fname, 
            ? as lname, 
            date('now') as regdate, 
            u.city as regplace, 
            ? as gender, 
            ? as f_fname,
            ? as f_lname,
            ? as m_fnmae,
            ? as m_lname
        from users u, births b
        where upper(u.uid) = upper(?)
        '''
        data = (child.get("fname"),child.get("lname"),child.get("gender"),\
            father.get("fname"),father.get("lname"),\
            mother.get("fname"),mother.get("lname"),session.get("uid"))
        c.execute(query,data)

        query = '''
        INSERT INTO persons
        select 
            ? as fname,
            ? as lname,
            ? as bdate,
            ? as bplace,
            m.address,
            m.phone
        from
            persons m
        where upper(m.fname) = upper(?) and upper(m.lname) = upper(?)
        '''
        data = (child.get("fname"),child.get("lname"),child.get("bdate"),child.get("bplace"),\
            mother.get("fname"),mother.get("lname"))
        c.execute(query,data)
    conn.commit()
    return jsonify(1)

def add_person(c,person):
    query = '''
    INSERT INTO persons
    VALUES (?,?,?,?,?,?)
    '''
    data = (person.get("fname"),person.get("lname"),person.get("bdate"),person.get("bplace"),person.get("address"),person.get("phone"))
    c.execute(query,data)

@app.route("/api/register_marriage",methods=["post"])
def register_marriage():
    if not session:
        abort(400)

    query = '''
        select fname,lname
        from persons p
        where upper(fname)=upper(?) and upper(lname) = upper(?)
    '''
    form = request.json    
    with connect_db() as conn:
        c = conn.cursor()
        more_info_required = []
        partners = {}
        for ptype in ["partner1","partner2"]:
            partner = form.get(ptype)
            c.execute(query,(partner.get("fname"),partner.get("lname")))
            row = c.fetchone()
            if row:
                partners[ptype] = partner
            elif partner.get("more_info"):
                add_person(c,partner)
                partners[ptype] = partner
            else:
                more_info_required.append(ptype)      
        if more_info_required:
            return jsonify({"more_info_required" : more_info_required})

        partner1 = partners["partner1"]
        partner2 = partners["partner2"]

        query = '''
        insert into marriages
        select 
            max(regno)+1, 
            date('now') as regdate, 
            u.city as regplace, 
            ? as p1_fname,
            ? as p1_lname,
            ? as p2_fnmae,
            ? as p2_lname
        from users u, marriages m
        where upper(u.uid) = upper(?)
        '''
        data = (partner1.get("fname"),partner1.get("lname"),\
            partner2.get("fname"),partner2.get("lname"),session.get("uid"))
        c.execute(query,data)
    conn.commit()
    return jsonify(1)
    
@app.route("/api/renew_registration",methods=["post"])
def renew_registration():

    form = request.json    
    with connect_db() as conn:
        c = conn.cursor()
        
        query = '''
            update registrations
            set expiry = case when expiry > date('now') then date(expiry,'+1 year') else date('now','+1 year') end
            where regno = ? '''
        data = (form.get("regno"),)
        c.execute(query,data)

        if c.rowcount > 0:
            return jsonify(1)
        else:
            return jsonify({"error" : "Registration # is not exist"})

        conn.commit()
        return jsonify(1)


@app.route("/api/process_bill",methods=["post"])
def process_bill():
    form = request.json    
    seller = form.get("seller")
    buyer = form.get("buyer")
    
    if not seller or not buyer:
        abort(400)
    with connect_db() as conn:
        c = conn.cursor()
        
        query = '''
            SELECT
                v.vin,
                p.plate,
                s.fname as sf,
                r.regno,
                b.fname as bf
            FROM
                vehicles v
                left join
                registrations p
                on p.plate = ?
                left join
                persons s
                on upper(s.fname) = upper(?) and upper(s.lname) = upper(?)
                left join
                registrations r
                on r.vin = v.vin and r.fname = s.fname and r.lname = s.lname and r.expiry > date('now')
                left join
                persons b
                on upper(b.fname) = upper(?) and upper(b.lname) = upper(?)
            WHERE
                v.vin = ?
            '''    
        data = (form.get("plate"),seller.get("fname"),seller.get("lname"),buyer.get("fname"),buyer.get("lname"),form.get("vin"))
        c.execute(query,data)
        row = c.fetchone()

        if not row:
            return jsonify({"error" : "VIN # is not exist"})
        if row["plate"]:
            return jsonify({"error" : "Plate already exist"})
        if not row["sf"]:
            return jsonify({"error" : "Seller is not exist"})
        if not row["regno"]:
            return jsonify({"error" : "Vehicle does not belongs to seller"})
        if not row["bf"]:
            return jsonify({"error" : "Buyer is not exist"})

        query = '''
            INSERT INTO registrations
            SELECT 
                max(regno) + 1 as regno,
                date('now') as regdate,
                date('now','+1 year') as expiry,
                ? as plate,
                ? as vin,
                ? as fname,
                ? as lname
            FROM registrations'''
        data = (form.get("plate"),form.get("vin"),buyer.get("fname"),buyer.get("lname"))
        c.execute(query,data)

        query = '''
            UPDATE registrations set expiry = date('now') where regno = ?
        '''
        data = (row["regno"],)
        c.execute(query,data)
        conn.commit()
        return jsonify(1)


@app.route("/api/process_payment",methods=["post"])
def process_payment():
    form = request.json
    with connect_db() as conn:
        c = conn.cursor()
        query = '''
            SELECT
                t.tno,
                t.fine - ifnull(sum(p.amount),0) as remain,
                ifnull(sum(case when p.pdate = date('now') then 1 else 0 end),0) as pay_today
            FROM
                tickets t
                left join
                payments p
                on p.tno = t.tno
            where t.tno = ?'''
        data = (form.get("tno"),)
        c.execute(query,data)
        row = c.fetchone()
        remain = row["remain"] - form.get("amount")
        if not row:
            return jsonify({"error" : "Ticket # is not exist"})
        if remain < 0:
            return jsonify({"error" : "Pay too much, ${} remains".format(row["remain"])})
        if (row["pay_today"]):
            return jsonify({"error" : "This ticket has been paid today"})

        query = '''
            INSERT INTO payments values (?,date('now'),?)
        '''
        data = (form.get("tno"),form.get("amount"))
        c.execute(query,data)
    conn.commit()
    return  jsonify({"remain" : remain})

@app.route("/api/driver_points",methods=["post"])
def driver_points():
    form = request.json
    with connect_db() as conn:
        c = conn.cursor()
        query = '''
            select
                p.fname,
                ifnull(sum(case when d.ddate > date('now','-2 years') then d.points else 0 end),0) as two_years_points,
                ifnull(sum(d.points),0) as lifetime_points
            from 
                persons p
                left join
                demeritNotices  d
                on p.fname = d.fname and p.lname = d.lname
            where upper(p.fname) = upper(?) and upper(p.lname) = upper(?)'''

        data = (form.get("fname"),form.get("lname"))
        c.execute(query,data)
        row = c.fetchone()

        if not row or not row["fname"]:
            return jsonify({"error" : "Driver is not exist"})
        session["driver"] = data
        del row["fname"]
        return jsonify({ "points" : row })

@app.route("/api/driver_tickets",methods=["get"])
def driver_tickets():
    driver = session.get("driver")
    if not driver:
        abort("400")
    query = '''
    SELECT
        t.tno,
        t.vdate as date,
        t.violation,
        t.fine,
        r.regno,
        v.make,
        v.model
    FROM
        tickets t
        left join
        registrations r
        on t.regno = r.regno
        left join
        vehicles v
        on r.vin = v.vin
    WHERE upper(r.fname) = upper(?) and upper(r.lname) = upper(?)
    ORDER BY date DESC
    '''
    unlimited = request.args.get('unlimited')
    if not unlimited:
        query += "LIMIT 6"

    with connect_db() as conn:
        c = conn.cursor()
        c.execute(query,driver)
        tickets = c.fetchall()
        return jsonify({ "tickets" : tickets[:5], "more" : len(tickets) > 5}) if not unlimited else ({"tickets" : tickets})

@app.route("/api/registration",methods=["get"])
def registration():
    regno = request.args.get('regno')
    query = '''
    SELECT
        p.fname || ' ' || p.lname as name,
        v.make,
        v.model,
        v.year,
        v.color
    FROM 
        registrations r
        left join
        persons p
        on p.fname = r.fname and p.lname = r.lname
        left join
        vehicles v
        on r.vin = v.vin
    WHERE r.regno = ?
    '''
    data = (regno,)
    with connect_db() as conn:
        c = conn.cursor()
        c.execute(query,data)
        row = c.fetchone()
        if not row:
            return jsonify({"error" : "Registration # is not exist"})        
        return jsonify({"r" : row})

@app.route("/api/issue_ticket",methods=["post"])
def issue_ticket():
    form = request.json
    with connect_db() as conn:
        c = conn.cursor()
        query = '''
        INSERT INTO tickets
        SELECT 
            max(tno) + 1 as tno,
            ? as regno,
            ? as fine,
            ? as violation,
            date('now') as vdate
        FROM
            tickets
        '''
        data = (form.get("regno"),form.get("fine"),form.get("violation"))
        c.execute(query,data)

        return jsonify(1)

@app.route("/api/find_car_owner",methods=["post"])
def find_car_owner():
    form = request.json
    with connect_db() as conn:
        c = conn.cursor()
        query = '''
        SELECT 
            v.make,
            v.model,
            v.year,
            v.color,
            r.plate,
            r.regdate,
            r.expiry,
            r.fname || " " || r.lname as owner
        FROM
            vehicles v
            left join
            registrations r on r.regno = (select regno from registrations where vin = v.vin order by regdate desc limit 1)
        WHERE
            r.regno is not null
        '''
        data = [] 
        for field in ["make","model","year","color","plate"]:
            value = form.get(field)
            if value:
                data.append(value)
                query += " and upper({}) = upper(?)".format(field)
        data = tuple(data)
        c.execute(query,data)
        return jsonify(c.fetchall())


@app.route('/')
@app.route('/<path:path>')
def index(path=None):
    return send_file('frontend/dist/index.html')

def main():
    if len(sys.argv) < 2:
        print("Usage: {} DATABASE_PATH".format(sys.argv[0]))
        return
    app.config["DB_PATH"] = sys.argv[1]
    try:
        conn = connect_db()
        if not conn:
            raise Exception()
    except:
        print("Error: failed connecting to the datebase")
        return
    app.run()
if __name__ == "__main__":
    main()