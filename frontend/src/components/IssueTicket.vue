<template>
    <div>
        <el-form :model="form1"  label-width="150px" ref="form1" @submit.native.prevent="submit1">
            <el-form-item label="Registration #" :rules="required" prop="regno">
                <el-input v-model.trim="form1.regno"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submit1">Submit</el-button>
            </el-form-item>
        </el-form>

        <template v-if="registration">
            <el-table :data="[registration]">
                <el-table-column
                    v-for='label in ["name","make","model","year","color"]'
                    :key="label"
                    :prop="label"
                    :label="_.upperFirst(label)"
                >
                </el-table-column>
            </el-table>

            <el-divider></el-divider>

            <el-form :model="form2"  label-width="150px" ref="form2">
                <el-form-item prop="date" label="Date" :rules="[required,notInFuture]">
                    <el-date-picker v-model.trim="form2.date" value-format="yyyy-MM-dd"></el-date-picker>
                </el-form-item>
                 <el-form-item prop="violation" label="Violation" :rules="[required]">
                    <el-input v-model.trim="form2.violation"></el-input>
                </el-form-item>
                 <el-form-item prop="fine" label="Fine" :rules="[required,positiveNum]">
                    <el-input type="number" v-model.trim.number ="form2.fine" ></el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submit2">Issue Ticket</el-button>
                </el-form-item>
            </el-form>
        </template>
    </div>
</template>

<script>
import {required,notInFuture,positiveNum} from "@/validators"
export default {
    data(){
        return {
            form1 : {
                regno : ""
            },
            form2 : {
                date : "",
                violation : "",
                fine : ""
            },
            registration : null,
            required,notInFuture,positiveNum
        }
    },
    methods : {
        async submit1(){
            try{
                await this.$refs.form1.validate();
            } catch {
                return
            }

            let {r,error} = await this.$api.get("registration?regno=" + this.form1.regno)

            if (r){
                this.registration = {...r,regno : this.form1.regno};
                this.$refs.form2.resetFields()
            } else if (error){
                this.$message({
                    showClose: true,
                    message: error,
                    type: 'error'
                })
            }
        },
        async submit2(){
            try{
                await this.$refs.form2.validate();
            } catch {
                return
            }

            let r = await this.$api.post("issue_ticket",{
                regno : this.registration.regno,
                ...this.form2
            })

            if (r == 1){
                this.$message({
                    showClose: true,
                    message: "Ticket Issued",
                    type: 'success'
                })
                this.$refs.form2.resetFields()
            } else if (r.error){
                this.$message({
                    showClose: true,
                    message: r.error,
                    type: 'error'
                })
            }
        }
    }
}
</script>