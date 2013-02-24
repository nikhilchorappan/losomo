function verify()

{

   document.input.action ="http://127.0.0.1:5000/search/{{name}}";

   document.input.submit();

}

function sendIt()

{

   document.input.action ="http://127.0.0.1:5000/tipreader/{{name}}";

   document.input.submit();

}

