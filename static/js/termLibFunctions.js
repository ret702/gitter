 <!--

  var helpPage = [
    "*************Commands*************",
	"help -Prints the help page",
	"login (username) (password)",
	"push (repo) (commit message) (branch)  -Pushes currently staged files to repo, type staged to see current file list",
	"staged ( (optional arg) clear -Clears staged files) -Prints which files are staged for push",
	"***********************************"
	
  ];

 var term;

 window.onload = termOpen;

 function termOpen() {
     if ((!term) || (term.closed)) {

         
         term = new Terminal({
             rows: 500,
             cols: 500,
             x: 0,
             y: 50,
             termDiv: 'termDiv',
             bgColor: '#000000',
             greeting: 'Welcome to Gitter %n%nEnter  A Command...  %nType help %nType login (username) (password) to start %n%n',
             handler: termHandler,
             exitHandler: termExitHandler
         });
         term.open();

         // dimm UI text
         var mainPane = (document.getElementById) ?
             document.getElementById('mainPane') : document.all.mainPane;
         if (mainPane) mainPane.className = 'lh15 dimmed';
     }
 }

 function getCookie(name) {
     var cookieValue = null;
     if (document.cookie && document.cookie != '') {
         var cookies = document.cookie.split(';');
         for (var i = 0; i < cookies.length; i++) {
             var cookie = jQuery.trim(cookies[i]);
             // Does this cookie string begin with the name we want?
             if (cookie.substring(0, name.length + 1) == (name + '=')) {
                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
             }
         }
     }
     return cookieValue;
 }


 function termHandler() {

     // default handler + exit
     this.newLine();
	 var cmd=this.lineBuffer;
     if (cmd != '') {
		if(cmd =='clear')
		{
			term.clear();
		}
		else if(cmd=='help')
		{
		  this.write(helpPage);
		}
		else{
         var csrftoken = getCookie('csrftoken');

         $.ajax({
             url: window.location.href, // the endpoint,commonly same url
             type: "POST", // http method
             data: {
                 csrfmiddlewaretoken: csrftoken,
                 command: this.lineBuffer
             }, // data sent with the post request

             // handle a successful response
             success: function(json) {
                 console.log(json); // another sanity check
                 //On success show the data posted to server as a message
                 term.type('Response: ' + json.result);
				 console.log(json.result)
                 term.lineBuffer
                 term.newLine();
                 term.prompt();
             },

             // handle a non-successful response
             error: function(xhr, errmsg, err) {
                 term.type('Response: ' +"Invalid method or attributes!");
				 console.log(xhr.responseText)
		         term.lineBuffer
                 term.newLine();
                 term.prompt();
             }
         });

		}

     term.lineBuffer
     term.newLine();
     term.prompt();

     }

 }

 function termExitHandler() {
     // reset the UI
     var mainPane = (document.getElementById) ?
         document.getElementById('mainPane') : document.all.mainPane;
     if (mainPane) mainPane.className = 'lh15';
 }




