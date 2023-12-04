<template>
    <textarea rows="3" cols="30" id="showMes" style="width:300px;height:500px;"></textarea>
    <div>{{ websockMsg }}</div>
    <br/>
    <label>名称</label>
    <input type="text" id="name"/>
    <br/>
    <label>消息</label>
    <input type="text" id="mes"/>
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
    mounted(){
        this.connect();
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
            setTimeout(()=>{
                document.getElementById("showMes").value+= this.websockMsg+"\n";
            },500)
           
        },


    }


}
</script>