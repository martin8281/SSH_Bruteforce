
        function scan() {

            var user = $(".user").val();
            var host =$(".host").val();
            var status=true;
            var passw=$(".passw").val();
            var port=$(".port").val();

            var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
            const txtExtensionRegex = /\.txt$/i;
            if(user==""){
                status=false;
                Message("please enter a user list path", 'Error', 'error');
             }
             if(passw==""){
                status=false;
                Message("please enter a password list path", 'Error', 'error');
             }
         if(host==""){
            status=false;
            Message("please enter a host name", 'Error', 'error');
         }
         if (!txtExtensionRegex.test(user) && user!="") {
           
            status=false;
            Message("Please enter the path of a .txt user file", 'Error', 'error');
        
        }
        if (!txtExtensionRegex.test(passw) && passw!="") {
           
            status=false;
            Message("Please enter the path of a .txt password file", 'Error', 'error');
        
        }
         var data={
           
            host:host,
            passw:passw,
            user:user,
            port:port
           

            
         }
      
if(status){

            $.ajax({
                type: 'POST',
                url: '/scan',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data:data,
                beforeSend: function() {
                    $(".start_scan").prop("disabled", true);
                    $(".stoped").hide();
                    $(".running").show();
                  
                },
                success: function (response) {
                    if (response.hasOwnProperty('task_id')) {
                        var taskId = response.task_id;
                        CheckScanStatus(taskId);
                    } else if (response.hasOwnProperty('error')) {
                        $(".start_scan").prop("disabled", false);
                        $(".stoped").show();
                        $(".running").hide();
                        Message(response.error, 'Error', 'error');
                    }
                },
                error: function (xhr, status, error) {
                    $(".start_scan").prop("disabled", false);
                    $(".stoped").show();
                    $(".running").hide();
               
                  
                    Message(error, 'Error', 'error');
                },
                dataType: 'json'
         
            });
        }
        }


        function CheckScanStatus(taskId) {
            var csrftoken = $("input[name=csrfmiddlewaretoken]").val();
 
            $.ajax({
                type: 'GET',
                url: '/CheckScanStatus',
                data: {
                    'task_id': taskId,
                    'job':"get_scan"
                },
                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: function (response) {
                    if (response.hasOwnProperty('status')) {
                        var status = response.status;
                        if (status === 'SUCCESS') {
                            Message('Scan Successfull', 'Success', 'success');  
                            $(".start_scan").prop("disabled", false);
                            $(".stoped").show();
                            $(".running").hide();
                    $(".scan-wifi-spin").hide();
                        } else if (status === 'FAILURE') {
                            $(".start_scan").prop("disabled", false);
                            $(".stoped").show();
                            $(".running").hide();
                            Message(response.traceback, 'Error', 'error');
                           
                        } else {
                            setTimeout(function () {
                                CheckScanStatus(taskId);
                            }, 2000);
                        }
                    } else {
                        setTimeout(function () {
                            CheckScanStatus(taskId);
                        }, 2000);
                    }
                },
                error: function (xhr, status, error) {
                    $(".start_scan").prop("disabled", false);
                    $(".stoped").show();
                    $(".running").hide();
                    Message(error, 'Error', 'error');
                    // console.log(error);
                    setTimeout(function () {
                        CheckScanStatus(taskId);
                    }, 2000);
                },
                dataType: 'json',
      
            });
        }

 

  

   

            
    //       </ul>
    //     </div>
    //   </div>




function worker(data){
    // var template='<div class="card"><div class="card-body"><h5 class="card-title">'
    // var template2=' <div class="card"><div class="card-body"><h5 class="card-title">Scan Result</h5><ul class="list-group list-group-flush">';
    // var template3='  </ul> </div></div>'
    $.each(data, function(index, dict) {

        if(dict.error==true){
            Message(dict.error_content, 'Error', 'error'); 
        }
        else {
            $('.result').append('<li class="list-group-item">Found User : '+dict.user+':'+dict.pass+'</li>');
            // if(dict.from==="robbot"){
            // if(dict.found){
            //     template+='Robbot.txt Found</h5><div class="accordion accordion-flush" id="accordionFlushExample">'
            //     template+='<div class="accordion-item">'
            //     template+='<h2 class="accordion-header" id="flush-headingOne">'
            //     template+=' <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-collapseOne" aria-expanded="false" aria-controls="flush-collapseOne">'
            //     template+='    Show Robot.txt Content'
            //     template+='  </button>'
            //     template+='  </h2>'
            //     template+=' <div id="flush-collapseOne" class="accordion-collapse collapse" aria-labelledby="flush-headingOne" data-bs-parent="#accordionFlushExample">'
            //     template+='   <div class="accordion-body">'+dict.content+'</div>'
            //     template+=' </div>'
            //     template+='  </div></div></div></div>'
        //     }else{
        //         template+='Robbot.txt Not Found</h5>'
        //         template+=' </div>'
        //         template+='  </div>'
        //     }
        // }
       
        // else if(dict.from==="scanner"){
            
        //       if(dict.response==200){
        //         template2+='<li class="list-group-item">Found <a href="'+dict.link+'">'+dict.link+'</a></li>'
        //         console.log('found'+dict.link);
        //       }else{
        //         template2+='<li class="list-group-item">Found (High Chance for Redirection Vulnerability)<a href="'+dict.link+'">'+dict.link+'</a></li>'
        //       }
      
        //     }
           
            
        // }  // Do whatever you want with the key-value pairs here
  
        }
      });
    //   template=template+template2+template3;
    //   $('.result').html(template);
}

		var socket = new WebSocket('ws://localhost:8000/ws/output/')
		socket.onmessage=function(event){
			var message=event.data;
            worker(JSON.parse(message));

		}
