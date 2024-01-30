var url = window.location.href
var currentRoadJs = "road1"

function change_road(i){
    var name_inter = $('input#'+i).val()
    currentRoadJs = name_inter

    // alert(currentRoadJs)
    console.log(name_inter)
    $.ajax({
        url:'/ajax/change_road',//url de votre file php pour recuperer les donnees
        type:"get",
        data:{option:name_inter},
        success: function(data){
           console.log('success '+data)
           console.log(data)
           $('#result').html(data)
        },
        error: function(jqXHR, textStatus, errorThrown) {
            console.log("error occured : "+textStatus, errorThrown)
        }
    });
}

function road_set_camera(){
    var camera_form = document.getElementById('camera_form')
    var selected = camera_form.options[camera_form.selectedIndex].value
    var road_name = currentRoadJs
    // alert(road_name)
    if (selected == 'default') NaN
    else {
        $.ajax({
            url:'/ajax/road_set_camera',//url de votre file php pour recuperer les donnees
            type:"get",
            data:{option:selected},
            success: function(data){
               console.log('success '+data)
               console.log(data)
               $('#show').html(data)

            //    alert(road_name)
                //if road setted avec succes, then load the given page for him
                $.ajax({
                    url:'/ajax/change_road',//url de votre file php pour recuperer les donnees
                    type:"get",
                    data:{option:road_name},
                    success: function(data){
                    console.log('success '+data)
                    console.log(data)
                    $('#result').html(data)
                    },
                    error: function(jqXHR, textStatus, errorThrown) {
                        console.log("error occured : "+textStatus, errorThrown)
                    }
                });

            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log("error occured : "+textStatus, errorThrown)
            }
        });

        // //then load the given page for him
        // $.ajax({
        //     url:'/ajax/change_road',//url de votre file php pour recuperer les donnees
        //     type:"get",
        //     data:{option:road_name},
        //     success: function(data){
        //     console.log('success '+data)
        //     console.log(data)
        //     $('#result').html(data)
        //     },
        //     error: function(jqXHR, textStatus, errorThrown) {
        //         console.log("error occured : "+textStatus, errorThrown)
        //     }
        // });
    }
}


if (url == "http://127.0.0.1:8000/setting") {
    // CANVAS
    var canvas = document.getElementById("canvas")
    var img = document.getElementById("img")

    var ctx = canvas.getContext("2d")
    ctx.font = "16px Arial"

    function road_choosen(){
        var road_form = document.getElementById('road_form')
        var selected = road_form.options[road_form.selectedIndex].value

        if (selected == 'default') NaN
        else {
            $.ajax({
                url:'/ajax/road_take_photo',//url de votre file php pour recuperer les donnees
                type:"get",
                data:{option:selected},
                success: function(data){
                    console.log('success '+data)
                    console.log(data)
                    if (data=='NaN') {
                        alert("Load first your road")

                        //Redirect the user first
                        var link = "http://127.0.0.1:8000/"
                        window.location.href = link
                        
                        //then load the given page for him
                        $.ajax({
                            url:'/ajax/change_road',//url de votre file php pour recuperer les donnees
                            type:"get",
                            data:{option:selected},
                            success: function(data){
                            console.log('success '+data)
                            console.log(data)
                            $('#result').html(data)
                            },
                            error: function(jqXHR, textStatus, errorThrown) {
                                console.log("error occured : "+textStatus, errorThrown)
                            }
                        });
                    } else {
                        $('#canvas').html(data)
                        
                        imgNew = document.getElementById('img')

                        // alert(imgNew)
                        // alert(imgNew)
                        // ctx.scale(0.5, 0.5)
                        // ctx.drawImage(imgNew, 0, 0, canvas.width, canvas.height)
                        imgNew.addEventListener("load", function(e){
                            ctx.drawImage(imgNew, 0, 0)
                        })

                        
                    }
                
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log("error occured : "+textStatus, errorThrown)
                }
            });

            // alert(img)
            // ctx.drawImage(img, 0, 0)
        }

        
        // check if canvas has a children
        // if(canvas.children.length > 0) {

        //     alert(img)
        //     ctx.drawImage(img, 0, 0)
        //     // img.addEventListener("load", function(e){
        //     //     ctx.drawImage(img, 0, 0)
        //     // })

        // } else {
        //     alert("has no children")
        // }

    }


    var coordTab = new Array()
    canvas.addEventListener("click", function(e){
        var cRect = canvas.getBoundingClientRect() //Get CSS pos, and width/height
        var canvasX = Math.round(e.clientX - cRect.left) //Substract the 'left' of the canvas
        var canvasY = Math.round(e.clientY - cRect.top) //from the X/Y positions to make
        var coord = [canvasX, canvasY]

        var coordZone = document.getElementById("coord")

        
        coordTab.push("["+coord+"]")

        coordZone.innerHTML = "["+coordTab+"]"
        // ctx.fillText("X: "+canvasX+", Y: "+canvasY, 10, 20)
        console.log("X: "+canvasX+", Y: "+canvasY, 10, 20)

        //Draw a red circle
        ctx.fillStyle = "red"
        ctx.beginPath()
        ctx.arc(canvasX, canvasY, 5, 0, 2 * Math.PI)
        ctx.fill()
    })

}

function sendCoord(){
    var road_form = document.getElementById('road_form')
    var selected = road_form.options[road_form.selectedIndex].value

    var coord = document.getElementById("coord").innerHTML

    if(selected != "default"){
        $.ajax({
            url:'/ajax/receive_coord',//url de votre file php pour recuperer les donnees
            type:"get",
            data:{
                coord:coord,
                road_name: selected
            },
            success: function(data){
               console.log('success '+data)
               console.log(data)
               alert(data)
            //    $('#result').html(data)

                //Then redirect the user in the configured road
                var link = "http://127.0.0.1:8000/"
                window.location.href = link
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log("error occured : "+textStatus, errorThrown)
            }
        });
    }
    
}

function onPageLoad(){
    var url = window.location.href
    //do this only on the root
    if(url == "http://127.0.0.1:8000/") {
        
        $.ajax({
            url:'/ajax/page_load',//url de votre file php pour recuperer les donnees
            type:"get",
            success: function(data){
               console.log('success '+data)
               console.log(data)
               $('#result').html(data)
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log("error occured : "+textStatus, errorThrown)
            }
        });
    }
} onPageLoad()

// var url = window.location.href
// //do this only on the root
// if(url == "http://127.0.0.1:8000/") {
//     var widthOld = result.clientWidth
//     var heightOld = result.clientHeight

//     // alert("heightOld : "+heightOld+" widthOld :"+widthOld)
//     function sizeChanged(){

//         var width = result.clientWidth
//         var height = result.clientHeight

//         if(width!=widthOld || height!=heightOld) {
//             widthOld = width
//             heightOld = height
            
//             $.ajax({
//                 url:'/ajax/frame_size',
//                 type:"get",
//                 data:{
//                     width:width,
//                     height:height
//                 },
//                 success: function(data){
//                     console.log('success '+data)
//                     console.log(data)
//                 },
//                 error: function(jqXHR, textStatus, errorThrown) {
//                     console.log("error occured : "+textStatus, errorThrown)
//                 }
//             })
//         }
//     }

//     setInterval(sizeChanged, 10)
// }

//do this only on the /setting
if(url == "http://127.0.0.1:8000/setting") {
    // var zoneRoadImage = $("#zoneRoadImage")

    var widthOld = zoneRoadImage.clientWidth
    var heightOld = zoneRoadImage.clientHeight

    function sizeChangedSetting(){
        
        var width = zoneRoadImage.clientWidth
        var height = zoneRoadImage.clientHeight

        if(width!=widthOld || height!=heightOld) {
            // alert("heightOld : "+heightOld+" widthOld :"+widthOld)
            widthOld = width
            heightOld = height
            
            // var zoneRoadImage = document.getElementById("zoneRoadImage")
            zoneRoadImage.setAttribute("min-width", width+"px")
            zoneRoadImage.setAttribute("max-width", width+"px")
        }
    }

    setInterval(sizeChangedSetting, 10)

}

// $(document).ready(function(){
//     var request

//         $("#filter").submit(function(event){
//             event.preventDefault();
        

//         if(request) {request.abort()}

//         var $form = $(this)

//         var $inputs = $form.find('select')

//         var serializedData = $form.serialize()

//         $inputs.prop("disabled", true)

//         request = $.ajax({
//             url:'../controllers/getTotal.php',
//             type:"post",
//             data:serializedData
//         })

//         request.done(function(response, textStatus, jqXHR){
//             console.log("Hooray, it work")
//         })

//         request.fail(function(jqXHR, textStatus, errorThrown){
//             console.error("Error occured : "+textStatus, errorThrown)
//         })
//     })
// })


$(document).ready(function(){
    //fonction pour recuperrer les donnees et les afficher
    // function change_road(name){
    //     $.ajax({
    //         url:'/ajax/change_road',//url de votre file php pour recuperer les donnees
    //         type:"get",
    //         data:{option:option},
    //         success: function(data){
    //             //Afficher les donnees dans les l'elemtn avec l'ID "contenu:
    //            // $('#contenu').html(data);
    //            console.log('success '+option)
    //         },
    //         error: function(jqXHR, textStatus, errorThrown) {
    //             console.log("error occured : "+textStatus, errorThrown)
    //         }
    //     });
    // }

    // $("#road").click(function(event){
    //     var n = $('input#name_inter').val()
    //     alert('salut petit '+n)
    // })
    
    
})