/*  THIS STYLE SHEET BELONGS TO SAVE WITH BLOOD APP
    Author: Ir Christian Scott -> Split Orange
    Date : 16 August 2018
*/

let markers = [];

$(document).ready(function(){
    $("#apcon-open-add-branch, #apcon-open-add-branch-else").click(function (e) {
        e.preventDefault();
        getUserCurrentLocation("apcon-branch-latitude", "apcon-branch-longitude", "apcon-search-location-input", "apcon-branch-town", "apcon-branch-country");
        setTimeout(function () {
            initMapUser();
        }, 1000);
        $("#apcon-add-new-branch").modal('show');
        $("#apcon-add-new-branch-else").modal({
            closable: false,
            onDeny: function () {
                $("#apcon-add-new-event-modal").click();
            },
            onApprove: function () {
                $("#apcon-search-location-input").val($("#apcon-search-location-input-else").val());
                $("#apcon-add-new-event-modal").click();
            }
        }).modal('show');
    });

    $("#apcon-add-new-admin-modal").openModal();
    $("#apcon-add-new-event-modal").openModal();

    $("#apcon-search-location-input, #apcon-search-location-input-else").keyup(function (e) {
        var key = e.charCode || e.keyCode || 0;
        if (key == 13) {
            e.preventDefault();
            var address = $(this).val();
            var geocoder = new google.maps.Geocoder();
            geocoder.geocode({
                'address': address
            }, function (results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    var from_lat = results[0].geometry.location.lat();
                    var from_long = results[0].geometry.location.lng();

                    $("#apcon-branch-latitude").val(from_lat);
                    $("#apcon-branch-longitude").val(from_long);
                }
            });
            setTimeout(function () {
                initMapUser();
            }, 1000);
        }
    });

    $("select.dropdown").dropdown()
    $("#apcon-new-branch-form").submitFormAjax();

    let today = new Date();

    $("#apcon-event-date").calendar({
        minDate: new Date(today.getFullYear(), today.getMonth(), today.getDate() - 5)
    });

    $("#apcon-event-description").froalaEditor(
        {
            placeholderText: "Event Description",
            toolbarInline: false,
            charCounterCount: false,
            toolbarButtons: ['bold', 'italic', 'underline', 'strikeThrough', 'color', 'fontSize', 'paragraphFormat', 'align', 'formatOL', 'formatUL', 'indent', 'outdent', 'emoticons', 'specialCharacters', 'insertLink', 'undo', 'redo']
        }
    );
});

jQuery.fn.submitFormAjax = function(){
    $(this).submit(function(e){
        e.preventDefault();
        if (window.event && window.event.keyCode == 13) e.preventDefault();

        let data = new FormData($(this)[0]);
        let action = $(this).attr("action");
        let method = $(this).attr("method");
        
        $.ajax({
            type: method,
            url: action,
            data: data,
            processData: false,
            contentType: false,
            success: function(response){
                console.log(response);
                if(response.type == 'success'){
                    showSuccessMessage(response.type, response.message);
                    if(response.redirect != null) window.location = response.redirect;
                } else {
                    showErrorMessage(response.type, response.message)
                }
            },
            error: function(_, t, e){
                showErrorMessage(t, e);
            }
        });
    });
}

jQuery.fn.openModal = function(){
    $(this).click(function(){
        $("[data-modal=" + $(this).attr("id") + "]").modal("show");
    });
}

function hideModal(container){
    $(container).modal('hide');
}

function showErrorMessage(id, message) {
    iziToast.error({
        id: id,
        timeout: 5000,
        title: 'Error',
        message: message,
        position: 'bottomLeft',
        transitionIn: 'bounceInLeft',
        close: false,
    });
}

function showSuccessMessage(id, message) {
    iziToast.success({
        id: id,
        timeout: 5000,
        title: 'Success',
        message: message,
        position: 'bottomLeft',
        transitionIn: 'bounceInLeft',
        close: false,
    });
}

function showInfoMessage(id, message) {
    iziToast.info({
        id: id,
        timeout: 5000,
        title: 'Info',
        message: message,
        position: 'bottomLeft',
        transitionIn: 'bounceInLeft',
        close: false,
    });
}

function getUserCurrentLocation(lt, lg, ad, tc, cc) {

    if (!navigator.geolocation) {
        return showErrorMessage('error_geolocation', 'Geolocation not supported by your browser');
    }
    navigator.geolocation.getCurrentPosition(function (position) {

        var geocoder = new google.maps.Geocoder();
        var location = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);

        geocoder.geocode({ 'latLng': location }, function (results, status) {

            if (status == google.maps.GeocoderStatus.OK) {

                var latitude = position.coords.latitude;
                var longitude = position.coords.longitude;
                var address = results[0].formatted_address;

                var length = results[0].address_components.length
                var country = results[0].address_components[length - 1]
                var town = results[0].address_components[length - 3]


                document.getElementById(lt).value = latitude;
                document.getElementById(lg).value = longitude;
                document.getElementById(ad).value = address;
                document.getElementById(tc).value = town.long_name;
                document.getElementById(cc).value = country.short_name;

                let inputElse = $("#apcon-search-location-input-else");

                if(inputElse != null){
                    inputElse.val(address);
                }

            } else {
                showErrorMessage("locate_user", status);
            }
        });
    }, function () {
        showErrorMessage("locate_user", 'Unable to fetch location');
    });
}

function initMapUser() {

    var latitude = parseFloat($("#apcon-branch-latitude").val());
    var longitude = parseFloat($("#apcon-branch-longitude").val());
    var address = $("#apcon-branch-address").val();
    var myLatLng = {
        lat: latitude,
        lng: longitude
    };

    map = new google.maps.Map(document.getElementById('apcon-branch-map-container'), {
        zoom: 16,
        center: myLatLng,
        gestureHandling: 'cooperative'
    });

    var marker = new google.maps.Marker({
        position: myLatLng,
        map: map,
        title: address
    });

    markers.push(marker);

    var geocoder = new google.maps.Geocoder();

    google.maps.event.addListener(map, 'click', function (event) {
        geocoder.geocode({
            'latLng': event.latLng
        }, function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                if (results[0]) {
                    var n_address = results[0].formatted_address;
                    var n_latitude = results[0].geometry.location.lat();
                    var n_longitude = results[0].geometry.location.lng();
                    var position = {
                        lat: n_latitude,
                        lng: n_longitude
                    }

                    $("#apcon-branch-latitude").val(n_latitude);
                    $("#apcon-branch-longitude").val(n_longitude);
                    $("#apcon-search-location-input").val(n_address);
                    
                    let inputElse = $("#apcon-search-location-input-else");

                    if (inputElse != null) {
                        inputElse.val(n_address);
                    }

                    clearMarkers();

                    var marker = new google.maps.Marker({
                        position: position,
                        map: map,
                        title: n_address
                    });
                    markers.push(marker);
                }
            } else {
                showErrorMessage("init_map", status);
            }
        });
    });
}

function setMapOnAll(map) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }
}

function clearMarkers() {
    setMapOnAll(null);
}

function deleteMarkers() {
    clearMarkers();
    markers = [];
}

function InitializePlaces(input) {
    var autocomplete = new google.maps.places.Autocomplete(document.getElementById(input));
    google.maps.event.addListener(autocomplete, 'place_changed', function () {
        autocomplete.getPlace();
    });
}