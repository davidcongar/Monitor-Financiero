tipo_ajuste=document.getElementById("tipo_de_ajuste").value
if(tipo_ajuste==="Salida"){
    document.getElementById("id_almacen").disabled = true;
    document.getElementById("id_producto").disabled = true;
    document.getElementById("tipo_de_ajuste").disabled = true;
    let cantidad_original=parseFloat(document.getElementById("cantidad").value);
    
    document.getElementById("dynamic_form").addEventListener("submit", function(event) {
        if(cantidad_original<parseFloat(document.getElementById("cantidad").value)){
            alert('La cantidad de ajuste no puede ser mayor que la cantidad disponible, '+cantidad_original);
            event.preventDefault(); // Correct way to cancel submit
            return; 
        }else{
            // Enable fields before submitting
            document.getElementById("id_almacen").disabled = false;
            document.getElementById("id_producto").disabled = false;
            document.getElementById("tipo_de_ajuste").disabled = false;
        }
    
      });
}
