$(function(){
    var items = $('#carousel').children();
    var len = items.length;
    var index = 0;
    var str = 0;
    var dots =  $('.dot').children();
    /*var dotsChild = $('.dot span');*/

    //自动播放函数autoPlay()

    function autoPlay(){
        $(items[index]).fadeIn(1000);

        function play(){
            $(dots).removeClass("active");
            if(index >=0 & index < len-1){
                $(items[index]).fadeOut(1500);
                index++;
                $(items[index]).fadeIn(1500);
                $(dots[index]).addClass("active");
            }else{
                $(items[index]).fadeOut(1500);
                index=0;
                $(items[index]).fadeIn(1500);
                $(dots[index]).addClass("active");
            };
            str = index;
        }

        setInterval(play,7000);

    }
    autoPlay();

    //点击左侧按钮的函数
    $(".left").click(function(){
        $(dots).removeClass("active");
        if(str == 0){
            $(items[str]).fadeOut(1500);
            str = len-1;
            $(items[str]).fadeIn(1500);
            $(dots[str]).addClass("active");
            index = str;

        }else{
            $(items[str]).fadeOut(1500);
            str --;
            $(items[str]).fadeIn(1500);
            $(dots[str]).addClass("active");
            index = str;
        }
    });
    //点击右侧按钮的函数
    $(".right").click(function(){
        $(dots).removeClass("active");
        if(str == len-1){
            $(items[str]).fadeOut(1500);
            str = 0;
            $(items[str]).fadeIn(1500);
            $(dots[str]).addClass("active");
            index = str;
        }else{
            $(items[str]).fadeOut(1500);
            str ++;
            $(items[str]).fadeIn(1500);
            $(dots[str]).addClass("active");
            index = str;
        }
    })
    //小圆点
    $(".dot span").click(function(){
        var num = $(this).index();
        $(dots).removeClass("active");
        $(dots[num]).addClass("active");
        $(items).fadeOut(1500);
        $(items[num]).fadeIn(1500);
        index = num;
    })
});
