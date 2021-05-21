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
        previewClass: "preview",

        //enctype: 'multipart/form-data',
        //uploadExtraData: function () {  // uploadExtraData携带附加参数，上传时携带csrftoken
        //    return {csrfmiddlewaretoken: $.cookie('csrftoken'), doc_uuid: $('[name=doc_uuid]').val()}
        //},
        initialPreview: [],　　// 默认预览设置，回显时会用到
        initialPreviewConfig: [],　　// 默认预览的详细配置，回显时会用到
    }).on("filebatchuploadsuccess", function (e, data, previewId, index) {
        console.log(data.response);
        $("#upload_img").attr("src", data.response.select_img)
        for (let i = 0; i < data.response.all_imgs.length; ++i) {
            let now_src = data.response.all_imgs[i];
            let now_img = $.createElement("img");
            now_img.attr("src", now_src);
            now_img.attr("alt", "Norway");
            $("#all-tabs-above").appendChild(now_img);
            /*
                <img id="img6" src="" alt="Norway" style="
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        transition: 0.3s;
        width: 200px;
        height: 200px;
        padding-top: 5px;
        padding-bottom: 5px;
        padding-right: 0px;
        padding-left: 5px;
        border-left-width: 0px;
        border-bottom-width: 0px;border-right-width: 0px;
    " width="200" height="200">
    */
        }

        for (let i = 0; i < data.response.tags.length; ++i) {
            var now_tag = data.response.tags[i];
            var now_li = $.createElement("li");
            now_li.attr("class", "nav-item");
            var now_a = $.createElement("a");
            now_a.attr("class", "nav-link");
            now_a.attr("id", now_tag + "-tab-tabs-above")
            now_a.attr("href", "#" + now_tag + "-tabs-above")
            now_a.attr("role", "tab-kv")
            now_a.attr("data-toggle", "tab");
            now_a.attr("aria-controls", now_tag);
            now_li.appendChild(now_a)
            $("#myTab-tabs-above").appendChild(now_li)

            var now_div = $.createElement("div");
            now_div.attr("class", "tab-pane fade");
            now_div.attr("id", now_tag + "-tabs-above");
            now_div.attr("role", "tabpanel");
            now_div.attr("aria-labelledby", now_tag + "-tab-tabs-above");

            for (let j = 0; j < data.response[now_tag]; ++j) {
                let now_src = data.response[now_tag][i];
                let now_img = $.createElement("img");
                now_img.attr("src", now_src);
                now_img.attr("alt", "Norway");
                now_div.appendChild(now_img)
            }

            $("#myTabContent-tabs-above").appendChild(now_div)
        }

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
