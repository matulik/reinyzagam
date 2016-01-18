function refresh() {
    var $dynamic_table = $("#dynamic_table");
    $.ajax({
        type: 'GET',
        url: '/rest/locations_list/',
        dataType: "json",
        success: function (data) {
            $dynamic_table.dynatable({
                dataset: {
                    records: data
                },
                features: {
                    pushState: false
                }

            });
            table_refresh(data)
        }
    });
}

function validation() {
    var test_name = true;
    var test_description = true;

    var name = $("#name").val();
    var description = $("#description").val();

    var dataString = 'name=' + name + '&description=' + description;

    if (name.length == 0) {
        if ($("#error_name").is(":hidden")) {
            $("#error_name").text("Błędna nazwa kategorii!");
            $("#error_name").slideDown("slow");
        }
        test_name = false
    }

    if (description.length == 0) {
        if ($("#error_description").is(":hidden")) {
            $("#error_description").text("Błędny opis kategorii!");
            $("#error_description").slideDown("slow");
        }
        test_description = false;
    }
    if (test_name == false || test_description == false) {
        if (test_name == true)
            $("#error_name").slideUp("fast");
        if (test_description == true)
            $("#error_description").slideUp("fast");
    }
    else {
        addData(dataString)
    }
}

function table_refresh(data) {
    var dynatable = $('#dynamic_table').data("dynatable");
    dynatable.records.updateFromJson({records: data});
    dynatable.records.init();
    dynatable.process();
    dynatable.dom.update();
}

function addData(dataString) {
    $.ajax({
        type: 'POST',
        url: '/rest/locations_list/',
        dataType: "json",
        data: dataString,
        success: function (data) {
            console.log("Added")
        }
    });
    refresh();
}

function trmouseclick(i) {
    var row = $("tr").get(i.rowIndex);
    if (row.className == "mouseover")
        row.className = "";
    else
        row.className = "mouseover";
    var ids = document.getElementsByClassName("mouseover");
}

function return_checked() {
    var ret_ids = [];
    var ids = document.getElementsByClassName("mouseover");
    for (var i = 0; i < ids.length; i++)
        ret_ids.push(ids.item(i).firstChild.textContent);
    return ret_ids;
}

function delData(ids) {
    for (var i = 0; i < ids.length; i++) {
        var url = '/rest/location_detail/' + ids[i].toString() + '/';
        $.ajax({
            type: 'DELETE',
            url: url,
            dataType: "json",
            success: function (data) {
                console.log("Deleted")
            }
        });
    }
    refresh();
}

$(document).ready(function () {
    refresh();
    $("#button_add").click(function () {
            validation();
        }
    );

    $("#button_del").click(function () {
            delData(return_checked())
        }
    );
});