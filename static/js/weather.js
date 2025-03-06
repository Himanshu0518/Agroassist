
  document.getElementById("todayBtn").addEventListener("click", function() {
            document.getElementById("today_weather").style.display = "block" ;
            document.getElementById("forecast").style.display = "none" ;
        } );

  document.getElementById("forecastBtn").addEventListener("click", function() {
      document.getElementById("today_weather").style.display = "none" ;
      document.getElementById("forecast").style.display = "block"
   } );
   