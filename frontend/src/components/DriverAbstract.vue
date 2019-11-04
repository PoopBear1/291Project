<template>
    <div>
        <el-form :model="form"  label-width="150px" ref="form">
            <fieldset>
                <legend >Driver</legend>
                <el-form-item label="First Name" :rules="required" prop="fname">
                    <el-input v-model.trim="form.fname"></el-input>
                </el-form-item>
                <el-form-item label="Last Name" :rules="required" prop="lname">
                    <el-input v-model.trim="form.lname"></el-input>
                </el-form-item>
            </fieldset>
        
            <el-form-item>
                <el-button type="primary" @click="submit">Submit</el-button>
            </el-form-item>
        </el-form>

        <template v-if="result.points">
            <el-divider></el-divider>
            <el-table
                :data="result.points"
            >
                <el-table-column
                    prop="two_years_points"
                    label="Points within 2 Years"
                >
                </el-table-column>
                <el-table-column
                    prop="lifetime_points"
                    label="Lifetime Points"
                >
                </el-table-column>
            </el-table>
            <el-divider></el-divider>
            <el-button type="primary" @click="getTickets()" v-if="!result.tickets">Show Tickets</el-button>
            <el-table
                v-else
                :data="result.tickets"
            >
                <el-table-column
                    prop="tno"
                    label="Ticket #"
                >
                </el-table-column>
                <el-table-column
                    prop="date"
                    label="Date"
                >
                </el-table-column>
                <el-table-column
                    prop="violation"
                    label="Violation"
                >
                </el-table-column>
                    <el-table-column
                    prop="regno"
                    label="Registration #"
                >
                </el-table-column>
                <el-table-column
                    prop="make"
                    label="Make"
                >
                </el-table-column>
                <el-table-column
                    prop="model"
                    label="Model"
                >
                </el-table-column>
            </el-table>
            <el-button type="primary" @click="getTickets(true)" style="margin-top : 1em" v-if="result.more">Show More Tickets</el-button>
        </template>
    </div>
</template>

<script>
import {required} from "@/validators"
export default {
    data(){
        return {
            form : {
                fname : "",
                lname : ""
            },
            result : {},
            required
        }
    },
    methods : {
        async submit(){
            try{
                await this.$refs.form.validate();
            } catch {
                return
            }

            let r = await this.$api.post("driver_points",this.form)

            if (r.points){
                this.result = {
                    points : [r.points],
                    tickets : null,
                    more : false
                }
            } else if (r.error){
                this.$message({
                    showClose: true,
                    message: r.error,
                    type: 'error'
                })
            }
        },
        async getTickets(unlimited = false){
            let {tickets,more} = await this.$api.get("driver_tickets" + (unlimited ? "?unlimited=1" : "") )
            this.$set(this.result,"tickets",tickets)
            this.$set(this.result,"more",more)
        }
    }
}
</script>