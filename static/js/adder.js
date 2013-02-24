    
    //automatic tag generation
    var singletag
    var taglist="";
    var tagprint
    function setTag()
    {
     singletag = document.getElementById('tag').value;
     tagprint=document.getElementById('tagPrint');
     tagprint.innerHTML = tagprint.innerHTML+"     "+singletag;
     taglist = taglist+","+singletag;
     taglist = taglist.substring(1);
     document.getElementById('taglist').value = taglist;
     taglist = ","+taglist;
     document.getElementById('tag').value ='';
    }

    //used for dynamically selecting the spark item(drop down)
    function show(selector) {
      var z= selector.value;
      var article = document.getElementsByTagName("div");
      for(var x=0; x<article.length; x++) {
        name = article[x].getAttribute("name");
        if (name == 'article') {
          if (article[x].id == z) {
            article[x].style.display = 'block';
          }else{
            article[x].style.display = 'none';
          }
        }
      }
    }
