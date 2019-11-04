import moment from "moment"
import _ from "lodash"
export const required = {
    required: true, 
    message: 'This field is required'
}
export const notInFuture = {
    validator: (_, value, callback) => {
        if (value > moment().format("YYYY-MM-DD")){
            return callback(new Error('Date cannot be later than today' ))
        }
        callback();
    }            
}
export const positiveNum = {
    validator : (rule,value,callback) => {
        if (!_.isNumber(value)){
            callback(new Error("This field must be a number"))
        } else if (value <= 0){
            callback(new Error("This field must be greater than 0"))
        } else {
            callback()
        }
    }
}