  let display_family = false;

  function toggle_family(family_form){
      if(display_family === "0"){ // Init from backend
        display_family = false;
      }
      display_family = !display_family;
      document.getElementById("family_form").innerHTML = display_family ? family_form : "";
      document.getElementById("toggle_family_button").innerHTML = display_family ? "family -" : "family +";
      }
