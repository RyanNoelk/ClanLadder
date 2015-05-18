
function SubmitFormReplay()
{
    var file = document.getElementById("file").value;
    var none = document.getElementById("no_replay_warning");
    var bad = document.getElementById("bad_file_warning");
    
    if (!file)
    {
        none.style.display = '';	
        bad.style.display = 'none';	
        return 0;
    }
        
    var array = file.split(',');
    for (var i = 0; i < array.length; i++) 
    {
        var loc_array = array[i].split('.');
        if (loc_array[loc_array.length-1] != 'SC2Replay')
        {
            bad.style.display = '';	
            none.style.display = 'none';	
            return 0;
        }
    }
    
    document.ReplayForm.submit();
    return 0;
}

function GetPlayerRaceAndCountry(RaceID, CountryID, name)
{
    var strname = document.getElementById(name).value;
    ajaxGet('/Matches/GetPlayerRaceAndCountry/'+strname+'/', function(content){
        var output = ''; 
        for (var property in content) 
        {
            output += content[property];
        }
        var array = output.split(',');
        var race = array[0]; 
        var country = array[1]; 
        
        $('#'+RaceID).val(race);
        $('#'+CountryID).val(country);
    });
}

function GetPlayerList(ids)
{
    ajaxGet('/Matches/GetPlayerList/', function(content){
        var output = '';
        for (var property in content) {
            output += content[property];
        }
        var array = output.split(',');
        BuildDropDown(ids, array);
    });
}

function BuildDropDown(ids, array)
{
    for (var i = 0; i < ids.length; i++)
    {
        $('#'+ids[i]).empty();
        var options = $('#'+ids[i]);
        options.append($("<option />").val('').text('Please Select a Player...'));
        options.append($("<option />").val('New').text('New'));
        $.each(array, function() {
            options.append($("<option />").val(this).text(this));
        });
    }
}

function SubmitFormText()
{
    var submit = true;
    
    $('#TextForm input[type="text"]').each(function(){
        if (!this.value)
        {
            if (this.id.indexOf("new_name") > -1)
            {
                if (document.getElementById(this.id.substring(0, this.id.length - 9)).value == 'New')
                {
                    submit = false;
                }
            }
            else
            {
                submit = false;
            }
        }
    });
    
    $('#TextForm select').each(function(){
        if (!this.value)
        {
            if (this.id.indexOf("new_name") > -1)
            {
                if (document.getElementById(this.id.substring(0, this.id.length - 9)).value == 'New')
                {
                    submit = false;
                }
            }
            else
            {
                submit = false;
            }
        }
    });
    
    if (submit)
        document.TextForm.submit();
    else
    {
        var obj = document.getElementById("form_text_warning");
        obj.style.display = '';	
    }
}

function ToggleChanges(text, rc, id)
{
    select = document.getElementById(id).value;
    
    if (select == '')
    {
        document.getElementById(text).style.display = 'None';
        document.getElementById(rc).style.display = 'None';
    }
    else if (select == 'New' || select == 'new')
    {
        document.getElementById(text).style.display = '';
        document.getElementById(rc).style.display = '';    
    }
    else
    {
        document.getElementById(text).style.display = 'None';
        document.getElementById(rc).style.display = '';        
    }
}

function CreateNewPlayerSelection(match_num, i, text)
{
    var ret_string = '<select id="'+match_num+'_'+text+'_'+i+'" name="'+match_num+'.'+text+'.'+i+'.old_name'+'" class="match_submit" OnChange=\'ToggleChanges("'+i+match_num+'text_'+text+'", "'+i+match_num+'rc_'+text+'", "'+match_num+'_'+text+'_'+i+'"); GetPlayerRaceAndCountry("'+match_num+'_'+text+'_'+i+'_race", "'+match_num+'_'+text+'_'+i+'_country", "'+match_num+'_'+text+'_'+i+'");\'></select>';
    
    ret_string += '<div style="display:none;" id="'+i+match_num+'text_'+text+'"><input type="text" placeholder="New Players Name" class="match_submit" id="'+match_num+'_'+text+'_'+i+'_new_name" name="'+match_num+'.'+text+'.'+i+'.new_name" value=""></div>';
    
    ret_string += '<div style="display:none;" id="'+i+match_num+'rc_'+text+'"><select id="'+match_num+'_'+text+'_'+i+'_race" name="'+match_num+'.'+text+'.'+i+'.race" class="match_submit"  style="width:50%;">'+RaceDropdownOptions()+'</select>';
    
    ret_string += '<select id="'+match_num+'_'+text+'_'+i+'_country" name="'+match_num+'.'+text+'.'+i+'.country" class="match_submit" style="width:50%;">'+CountryDropdownOptions()+'</select></div>';
    
    return ret_string;
}

function ChangeBoxes(w, l, text, match_num)
{
    var wid = document.getElementById(w);
    var lid = document.getElementById(l);
    
    var wid_innerHTML = '';
    var lid_innerHTML = '';
      
    for (i=0; i<(text); i++)
    {
        wid_innerHTML += CreateNewPlayerSelection(match_num, i, 'winners');
        lid_innerHTML += CreateNewPlayerSelection(match_num, i, 'losers');
        
        if (i < text-1)
        {
            wid_innerHTML += '<br><br>';
            lid_innerHTML += '<br><br>';
        }
    }
    
    wid.innerHTML = wid_innerHTML;
    lid.innerHTML = lid_innerHTML;
    
    var ids = [];
    for (i=0; i<(text); i++)
    {
        ids.push(match_num+'_winners_'+i);
        ids.push(match_num+'_losers_'+i);
    }
    GetPlayerList(ids);
}

function modify_qty() 
{
    var qty = document.getElementById('qty').value;
    var new_qty = parseInt(qty,10) + 1;    
    document.getElementById('qty').value = new_qty;
    return new_qty;
}

function DeleteRow()
{
    var mytable = document.getElementById('Manual_Match');
    var count = 0;
    var inputs = document.getElementsByTagName('input');
    for (var i = 0, j = inputs.length; i<j; i++) 
    {
        var input = inputs[i];
        
        if (input.type && input.type === 'checkbox' && input.checked) 
        {
            var obj = input.getAttribute('id');
            var rowIndex = document.getElementById(obj).rowIndex;
            
            mytable.deleteRow(rowIndex);
            i = 0;
        }
    }
}
  
function addNewRow()
{
    var table = document.getElementById('Manual_Match');
    var tr = table.insertRow(-1);
    
    var counter = modify_qty();
    tr.setAttribute('id', counter);
    
    var td = tr.insertCell();
    td.innerHTML= '<input type=\"checkbox\" id=\"' + counter + '\" name=\"counter\"/>';

    td = tr.insertCell();
    td.innerHTML= '<select name="type" class="match_submit" OnChange="ChangeBoxes(\''+counter+'winners\',\''+counter+'losers\', this.value, '+counter+')"><option value="1">1v1</option><option value="2">2v2</option><option value="3">3v3</option><option value="4">4v4</option></select>';

    td = tr.insertCell();
    td.innerHTML= '<input type="text" placeholder="Map Name" name="'+counter+'.map" class="match_submit"/>';

    td = tr.insertCell();
    td.setAttribute('id', counter+'winners');
    
    td = tr.insertCell();
    td.setAttribute('id', counter+'losers');
    
    ChangeBoxes(counter+'winners', counter+'losers', 1, counter);
}