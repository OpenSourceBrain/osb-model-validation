function total_membrane_area(cell)

  float totalarea = 0
  float totallength = 0
  
  str name
  float area
  float PI = 3.14159265359
  
  foreach name ({el {cell}/##[][TYPE=compartment],{cell}/##[][TYPE=symcompartment]})
  
    float length = {getfield {name} len}
  
    if (length == 0)
        area = {PI}*{getfield {name} dia}*{getfield {name} dia}
    else
        area = {PI}*{getfield {name} dia}*{getfield {name} len}
        totallength = totallength + length
    end
  
    totalarea = totalarea + area
    //echo "Compartment: " {name} ", area: " {area} ", length: " {length}", diam: " {getfield {name} dia}
  
  end
  return {totalarea}
end
