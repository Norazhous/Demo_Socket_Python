<template>
    <textarea rows="3" cols="30" id="showMes" style="width:300px;height:500px;"></textarea>
    <br/>
    <label>名称</label>
    <input type="text" id="name"/>
    <br/>
    <label>消息</label>
    <input type="text" id="mes"/>
    <div>{{ websockMsg }}</div>
    <button @click="sendMeg();">发送</button>
    <button @click="connect()">connect</button>
</template>

<script>
export default{
    name:"websocket",
    data(){
        return{
            
        }
    },
    watch:{
    },
    computed:{
        websockMsg(){
            return this.$store.getters.GETreceivedData;
        },

    },
    methods:{
        connect(){
            if ("WebSocket" in window) {
                this.$store.dispatch('WEBSOCKET_INIT_ACTION')
            }else{
                alert("The browser is not support WebSocket");
            }
        },
        sendMeg(){
            let message=document.getElementById("name").value+":"+document.getElementById("mes").value;
            document.getElementById("showMes").value+=message+"\n\n";
            this.$store.dispatch("WEBSOCKET_REIVE_ACTION",message);
            
            document.getElementById("showMes").value+= this.websockMsg+"\n";
        }
    }


}
</script>