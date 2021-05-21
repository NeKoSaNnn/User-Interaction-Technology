$(document).ready(function () {
    $("#search_bar").hide();
    $('#search_input').fileinput({
        theme: "fas",
        //browseClass:"btn btn-primary btn-block",
        //language: 'zh',     // 设置中文，需要引入locales/zh.js文件
        uploadUrl: 'imgUpload',     // 上传路径 *****************************************
        maxFileSize: 0,     // 上传文件大小限制，触发 msgSizeTooLarge 提示
        previewFileType: "image",
        browseClass: "browser-btn-solid-lg",
        browseLabel: "",
        browseTitle: "Select",
        browseIcon: "<i class=\"fa fa-image\"></i> ",
        removeClass: "remove-btn-solid-lg",
        removeLabel: "",
        removeTitle: "Delete",
        //removeIcon: "<i class=\"fa fa-trash\"></i> ",
        uploadClass: "upload-btn-solid-lg",
        uploadLabel: "",
        uploadIcon: "<i class=\"fa fa-search\"></i> ",
        uploadTitle: "Search",
        cancelClass: "cancel-btn-solid-lg hidden",
        cancelLabel: "",
        cancelTitle: "Cancel",
        allowedFileExtensions: ['jpg', 'jpeg', 'jpe', 'gif', 'png', 'pns', 'bmp', 'png', 'tif', 'tiff', '.gif', '.webp', '.pjp', '.xbm', '.svg', '.ico'],
        // {name}：将被上传的文件名替换，{size}：将被上传的文件大小替换，{maxSize}：将被maxFileSize参数替换。
        //msgSizeTooLarge: '"{name}" ({size} KB) 超过允许的最大上传大小 {maxSize} KB。请重新上传!',
        showPreview: true,  // 展示预览
        showBrowse: true,
        showUpload: true,   // 是否显示上传按钮
        showRemove: true,
        showCaption: true,  // 是否显示文字描述
        showClose: false,   // 隐藏右上角×
        uploadAsync: false, // 是否异步上传 ********************************************
        //initialPreviewShowDelete: true, // 预览中的删除按钮
        autoReplace: true,  // 达到最大上传数时，自动替换之前的附件
        required: true,
        validateInitialCount: true,
        maxFileCount: 1,
        msgPlaceholder: "Select file to search !",
        previewClass:"preview",

        //enctype: 'multipart/form-data',
        //uploadExtraData: function () {  // uploadExtraData携带附加参数，上传时携带csrftoken
        //    return {csrfmiddlewaretoken: $.cookie('csrftoken'), doc_uuid: $('[name=doc_uuid]').val()}
        //},
        initialPreview: [],　　// 默认预览设置，回显时会用到
        initialPreviewConfig: [],　　// 默认预览的详细配置，回显时会用到
    }).on("filebatchuploadsuccess", function (e, data, previewId, index) {
        console.log(data.response.image0);
        $("#img0").attr("src", data.response.image0);
        $("#img1").attr("src", data.response.image1);
        $("#img2").attr("src", data.response.image2);
        $("#img3").attr("src", data.response.image3);
        $("#img4").attr("src", data.response.image4);
        $("#img5").attr("src", data.response.image5);
        $("#img6").attr("src", data.response.image6);
        $("#img7").attr("src", data.response.image7);
        $("#img8").attr("src", data.response.image8);
        $('#table').show();
        $('#clear').show();
    }).on('filebrowse', function (event) {
        $('#search_input').fileinput("clear");
    });
});

function myFunction() {
    document.getElementById("predictedResult").innerHTML = "";
    $('#clear').hide();
}

$("#change_to_search").click(function () {

    $(this).fadeOut(200);
    setTimeout(function () {
        $(this).css("display", "none");
    }, 200);
    $("#search_bar").fadeIn(2500);

})

function search() {

    $('#load').show();

    $("form").submit(function (evt) {
        //$('#loader-icon').show();

        evt.preventDefault();

        //$('#loader-icon').show();
        var formData = new FormData($(this)[0]);

        $.ajax({
            url: 'imgUpload',
            type: 'POST',
            data: formData,
            //async: false,
            cache: false,
            contentType: false,
            enctype: 'multipart/form-data',
            processData: false,

            success: function (response) {
                $('#load').hide();
                $('#row1').show();
                //$('#clear').show();
                //console.log(response[1]);
                //document.getElementById("predictedResult").innerHTML= response;
                document.getElementById("img0").src = response.image0;
                document.getElementById("img1").src = response.image1;
                document.getElementById("img2").src = response.image2;
                document.getElementById("img3").src = response.image3;
                document.getElementById("img4").src = response.image4;
                document.getElementById("img5").src = response.image5;
                document.getElementById("img6").src = response.image6;
                document.getElementById("img7").src = response.image7;
                document.getElementById("img8").src = response.image8;
                $('#table').show();
                $('#clear').show();


            }
        });
        return false;
    })
}
