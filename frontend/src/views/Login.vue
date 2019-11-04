<template>
    <el-container>
        <el-main>
            <el-card>
                <el-form ref="form" :model="form" label-width="120px">
                    <el-form-item label="UID">
                      <el-input v-model="form.uid" name="uid"></el-input>
                    </el-form-item>
                    <el-form-item label="Password">
                      <el-input v-model="form.pwd" type="password" name="pwd"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="onSubmit">Login</el-button>
                    </el-form-item>
                </el-form>
            </el-card>
        </el-main>
    </el-container>
</template>

<script>
    export default {
        data: function() {
            return { 
                form : {
                    uid : "",
                    pwd : ""
                }
            }
        },
        methods : {
            async onSubmit(){
                let user = await this.$api.post("login",this.form)
                if (user){
                    this.$store.user = user;
                    this.$router.push("/")
                } else {
                    if(this.msg) this.msg.close()
                    this.msg = this.$message({
                        showClose: true,
                        message: 'Wrong UID / password',
                        type: 'error'
                    })
                }
            }
        }
    }
</script>

