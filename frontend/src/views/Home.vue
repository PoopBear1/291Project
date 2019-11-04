<template>
    <el-container class="home">
        <el-header>
            <el-menu default-active="0" mode="horizontal" @select="menuSelect">
                <el-menu-item v-for="({label},index) in functions" :index="''+index" :key="index">{{label}}</el-menu-item>
                <el-submenu index="sub" style="float:right">
                    <template slot="title">Welcome, {{$store.user.name}}</template>
                    <el-menu-item index="logout">Logout</el-menu-item> 
                </el-submenu>
            </el-menu>
        </el-header>
        <el-main>
            <el-card v-if="current" :header="current.label">
                <keep-alive>
                <component :is="current.component"></component>
                </keep-alive>
            </el-card>
        </el-main>
    </el-container>
</template>

<script>
import RegisterBirth from "@/components/RegisterBirth.vue"
import RegisterMarriage from "@/components/RegisterMarriage.vue"
import RenewRegistration from "@/components/RenewRegistration.vue"
import ProcessBill from "@/components/ProcessBill.vue"
import ProcessPayment from "@/components/ProcessPayment.vue"
import DriverAbstract from "@/components/DriverAbstract.vue"
import IssueTicket from "@/components/IssueTicket.vue"
import FindCarOwner from "@/components/FindCarOwner.vue"
export default {
    data(){
        return {
            index : 0
        }
    },
    methods : {
        menuSelect(index){
            if (index == "logout"){
                this.$api("logout");
                this.$store.user = null;
                this.$router.push("/login");
            } else {
                this.index = index;
            }
        }
    },
    computed : {
        functions(){
            if (this.$store.user.type == 'a'){
                return [
                    { label : "Register New Birth", component : RegisterBirth },
                    { label : "Register Marriage", component : RegisterMarriage },
                    { label : "Renew Vehicle Registration", component : RenewRegistration },
                    { label : "Process a Bill of Sale", component : ProcessBill },
                    { label : "Process a Payment", component : ProcessPayment },
                    { label : "Get Driver Abstract", component : DriverAbstract }
                ]
            } else if (this.$store.user.type == 'o'){
                return [
                    { label : "Issue a Ticket" , component : IssueTicket },
                    { label : "Find a Car Owner", component : FindCarOwner },
                ]
            }
            return [];
        },
        current(){
            return this.functions[this.index];
        }
    }
}
</script>

<style>
    fieldset {
        margin-bottom : 1em;
        border: 2px #E4E7ED solid;
        border-radius: 1em;
        padding-left : 0px;
        margin-left: -2px;
    }
    legend {
        margin-left: 1em;
    }
    legend {
        color : #303133;
    }
    .home .el-form-item .el-button {
        float : right;
    }
</style>