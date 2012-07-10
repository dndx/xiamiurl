void((function(){
    var url = window.location.href;
    var result = /^http:\/\/www\.xiami\.com\/song\/(\d+)$/.exec(url);
    if (result){
        window.location.replace('http://xmurl.sinaapp.com/song/' + result[1]);
        return false;
    }
    var result = /^http:\/\/www\.xiami\.com\/album\/(\d+)$/.exec(url);
    if (result){
        window.location.replace('http://xmurl.sinaapp.com/album/' + result[1]);
        return false;
    }
    var result = /^http:\/\/www\.xiami\.com\/song\/showcollect\/id\/(\d+)$/.exec(url);
    if (result){
        window.location.replace('http://xmurl.sinaapp.com/collect/' + result[1]);
        return false;
    }
    alert('不是合法的虾米播放页！');
})())
