$(document).ready(function(){
  console.log('document ready');
  load_songList();
});

function load_songList() {
  console.log('load_songList');
  $.get("load_index", function(data, status){
    $('.ViolinSpan').html(makeUL(data['Violin']));
    $('.ClarinetSpan').html(makeUL(data['Clarinet']));
  });
}

function makeUL(array) {
    var list = document.createElement('ul');
    for (var i = 0; i < array.length; i++) {
        var a = document.createElement('a');
        a.href = '/get_similar_songs/' + array[i][1];
        a.target = '_blank';
        var item = document.createElement('li');
        item.appendChild(document.createTextNode(array[i][0]));
        a.appendChild(item);
        list.appendChild(a);
    }
    return list;
}
