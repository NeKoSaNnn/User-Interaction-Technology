(function ($) {
    "use strict";
    toastr.options = {
        "closeButton": false,
        "newestOnTop": true,
        "progressBar": false,
        "positionClass": "toast-top-right",
        "preventDuplicates": false,
        "showDuration": "100",
        "hideDuration": "1000",
        "timeOut": "2500",
        "extendedTimeOut": "1000",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    };

    $("#search_bar").hide();
    $("#mytab").hide();
    $("#clear_div").css("display", "none");

    var stars = 800; /*星星的密集程度，数字越大越多*/
    var $stars = $(".stars");
    var r = 800; /*星星的看起来的距离,值越大越远,可自行调制到自己满意的样子*/
    for (var i = 0; i < stars; i++) {
        var $star = $("<div/>").addClass("star");
        $stars.append($star);
    }
    $(".star").each(function () {
        var cur = $(this);
        var s = 0.2 + (Math.random() * 1);
        var curR = r + (Math.random() * 300);
        cur.css({
            transformOrigin: "0 0 " + curR + "px",
            transform: " translate3d(0,0,-" + curR + "px) rotateY(" + (Math.random() * 360) +
                "deg) rotateX(" + (Math.random() * -50) + "deg) scale(" + s + "," + s + ")"

        })
    })


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
        toastr.success("Image Search Complete !");
        $("#upload_img").attr("src", data.response.select_img)
        for (let i = 0; i < data.response.all_imgs.length; ++i) {
            let now_src = data.response.all_imgs[i];
            let now_img = $("<img src=\"\" alt=\"Norway\" style=\"\n" +
                "        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);\n" +
                "        transition: 0.3s;\n" +
                "        width: 200px;\n" +
                "        height: 200px;\n" +
                "        padding-top: 5px;\n" +
                "        padding-bottom: 5px;\n" +
                "        padding-right: 0px;\n" +
                "        padding-left: 5px;\n" +
                "        border-left-width: 0px;\n" +
                "        border-bottom-width: 0px;border-right-width: 0px;\n" +
                "    \" width=\"200\" height=\"200\">");
            now_img.attr("src", now_src);
            let now_a = $("<a class=\"popup-with-move-anim pop\"></a>")
            now_a.attr("href", "#" + now_src.split("\\")[1].split(".")[0])
            now_a.append(now_img)
            $("#all-tabs-above").append(now_a).addClass("show active");

            let now_div = $("<div class=\"lightbox-basic zoom-anim-dialog mfp-hide\">\n" +
                "    <div class=\"row\">\n" +
                "        <button title=\"Close (Esc)\" type=\"button\" class=\"mfp-close x-button\">×</button>\n" +
                "        <div class=\"col-lg-12\" style=\"text-align:center;margin:auto 0;\">\n" +
                "            <img src='' class=\"img-fluid\" alt='image'>\n" +
                "        </div>\n" +
                "    </div>\n" +
                "</div>")
            now_div.attr("id", now_src.split("\\")[1].split(".")[0]);
            now_div.find(".img-fluid").attr("src", now_src);
            $("#light_box").append(now_div);

            $('.popup-with-move-anim').magnificPopup({
                type: 'inline',
                fixedContentPos: false, /* keep it false to avoid html tag shift with margin-right: 17px */
                fixedBgPos: true,
                overflowY: 'auto',
                closeBtnInside: true,
                preloader: false,
                midClick: true,
                removalDelay: 300,
                mainClass: 'my-mfp-slide-bottom'
            });
        }
        for (let i = 0; i < Math.min(data.response.all_tags.length, 9); ++i) {
            let now_tag = data.response.all_tags[i];
            let now_li = $("<li></li>");
            now_li.addClass("nav-item otherli");
            let now_a = $("<a></a>");
            now_a.addClass("nav-link");
            now_a.attr("id", now_tag + "-tab-tabs-above")
            now_a.attr("href", "#" + now_tag + "-tabs-above")
            now_a.attr("role", "tab-kv")
            now_a.attr("data-toggle", "tab");
            now_a.attr("aria-controls", now_tag);
            now_a.text(now_tag);
            now_li.append(now_a)
            $("#myTab-tabs-above").append(now_li)

            var now_div = $("<div></div>");
            now_div.addClass("tab-pane fade otherscontent");
            now_div.attr("id", now_tag + "-tabs-above");
            now_div.attr("role", "tabpanel");
            now_div.attr("aria-labelledby", now_tag + "-tab-tabs-above");

            for (let j = 0; j < data.response[now_tag].length; ++j) {
                let now_src = data.response[now_tag][j];
                let now_img = $("<img src=\"\" alt=\"Norway\" style=\"\n" +
                    "        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);\n" +
                    "        transition: 0.3s;\n" +
                    "        width: 200px;\n" +
                    "        height: 200px;\n" +
                    "        padding-top: 5px;\n" +
                    "        padding-bottom: 5px;\n" +
                    "        padding-right: 0px;\n" +
                    "        padding-left: 5px;\n" +
                    "        border-left-width: 0px;\n" +
                    "        border-bottom-width: 0px;border-right-width: 0px;\n" +
                    "    \" width=\"200\" height=\"200\">");
                now_img.attr("src", now_src);
                let now_a = $("<a class=\"popup-with-move-anim\"></a>")
                now_a.attr("href", "#" + now_src.split("\\")[1].split(".")[0])
                now_a.append(now_img)
                now_div.append(now_a)
            }

            $("#myTabContent-tabs-above").append(now_div);

            $('.popup-with-move-anim').magnificPopup({
                type: 'inline',
                fixedContentPos: false, /* keep it false to avoid html tag shift with margin-right: 17px */
                fixedBgPos: true,
                overflowY: 'auto',
                closeBtnInside: true,
                preloader: false,
                midClick: true,
                removalDelay: 300,
                mainClass: 'my-mfp-slide-bottom'
            });
        }

        $("#mytab").fadeIn(300);
        $("html,body").animate({scrollTop: $("#mytab").offset().top}, 800);
        $("#clear_div").css("display", "")
    }).on('filebrowse', function (event) {
        $("#myTabContent-tabs-above").children(".otherscontent").remove();
        $("#all-tabs-above").children().remove();
        $("#myTab-tabs-above").children(".otherli").remove();
        $("#light_box").children().remove()
        $('#search_input').fileinput("clear");
        $("#mytab").hide();
        $("#clear_div").css("display", "none")
    }).on('fileselect', function (event) {
        $("#myTabContent-tabs-above").children(".otherscontent").remove();
        $("#all-tabs-above").children().remove();
        $("#myTab-tabs-above").children(".otherli").remove();
        $("#light_box").children().remove()
        $("#mytab").hide();
        $("#clear_div").css("display", "none")
    });

    /* Lightbox - Magnific Popup */
})(jQuery);

$("#clear_btn").click(function () {
    return new Promise(function (resolve, reject) {
        $.confirm({
            title: 'Confirm!',
            content: "Are you sure to clear ?",
            type: 'red',
            buttons: {
                yes: {
                    btnClass: 'btn-danger text-white',
                    keys: ['enter'],
                    action: function () {
                        toastr.info("Clear ~ ");
                        resolve();
                        $("#myTabContent-tabs-above").children(".otherscontent").remove();
                        $("#all-tabs-above").children().remove();
                        $("#myTab-tabs-above").children(".otherli").remove();
                        $("#light_box").children().remove()
                        $('#search_input').fileinput("clear");
                        $("#mytab").hide();
                        $("#clear_div").css("display", "none")
                    }
                },
                no: {
                    btnClass: 'btn-default text-black',
                    keys: ['enter'],
                    action: function () {
                        resolve();
                    }
                }
            }
        });
    });

});

$("#change_to_search").click(function () {
    $("#mytitle").animate({top: '3rem'}, 1000);
    $(this).fadeOut(200);
    setTimeout(function () {
        $(this).css("display", "none");
    }, 200);
    $("#search_bar").fadeIn(2500);
});
