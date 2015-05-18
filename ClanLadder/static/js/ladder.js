
function toggle(obj_id)
{
    var obj = document.getElementById(obj_id);
    if(obj.style.display == 'none')
        obj.style.display = '';		
    else
        obj.style.display = 'none';	
}


function adv_toggle(obj_id,btn_id,btn_value)
{
    var obj = document.getElementById(obj_id);
    var btn = document.getElementById(btn_id);
    if(obj.style.display == 'none')
    {
        obj.style.display = '';				
        btn.innerHTML = '[-] '+ btn_value;
    }			
    else
    {
        obj.style.display = 'none';
        btn.innerHTML = '[+] '+ btn_value;	
    }			
}

$(document).ready(function() {
    $('#Past_Games').dataTable( {     
        "paging":   false,
        "ordering": false,
        "searching": false,
        "info":     false
    } );
} );
$(document).ready(function() {
    $('#Ladder_table1').dataTable( {
        responsive: true,
        "order": [[ 0, "desc" ]]
    } );
} );
$(document).ready(function() {
    $('#1_data_table').dataTable( {
        "paging":   false,
        responsive: true,
        "order": [[ 0, "desc" ]],    
        columnDefs: [
            { type: 'alt-string', targets: 1 },
            { type: 'alt-string', targets: 3 }
        ]
    } );
} );
$(document).ready(function() {
    $('#2_data_table').dataTable( {
        "paging":   false,
        responsive: true,
        "order": [[ 0, "desc" ]],    
        columnDefs: [
            { type: 'alt-string', targets: 1 },
            { type: 'alt-string', targets: 3 }
        ]
    } );
} );
$(document).ready(function() {
    $('#3_data_table').dataTable( {
        "paging":   false,
        responsive: true,
        "order": [[ 0, "desc" ]],    
        columnDefs: [
            { type: 'alt-string', targets: 1 },
            { type: 'alt-string', targets: 3 }
        ]
    } );
} );
$(document).ready(function() {
    $('#4_data_table').dataTable( {
        "paging":   false,
        responsive: true,
        "order": [[ 0, "desc" ]],    
        columnDefs: [
            { type: 'alt-string', targets: 1 },
            { type: 'alt-string', targets: 3 }
        ]
    } );
} );
$(document).ready(function() {
    $('#5_data_table').dataTable( {
        "paging":   false,
        responsive: true,
        "order": [[ 0, "desc" ]],    
        columnDefs: [
            { type: 'alt-string', targets: 1 },
            { type: 'alt-string', targets: 3 }
        ]
    } );
} );
$(document).ready(function() {
    $('#6_data_table').dataTable( {
        "paging":   false,
        responsive: true,
        "order": [[ 0, "desc" ]],    
        columnDefs: [
            { type: 'alt-string', targets: 1 },
            { type: 'alt-string', targets: 3 }
        ]
    } );
} );