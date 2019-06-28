$(document).ready(function(){
  load_similar_songs();
});

function load_similar_songs() {
  $.get("/get_similar_songs", function(data, status){
    console.log('here 1');
    console.log('data: ' + JSON.stringify(data));
    console.log('here 2');
    var dataSet = data.map(function(a) {
      console.log('here 1' + JSON.stringify(a));
      return [a.songname, a.similarity];
    });
    console.log('here 3');
    console.log('dataSet: ' + JSON.stringify(dataSet));
    $('#similar_songs_table').DataTable( {
      data: dataSet,
      columns: [  { title: "Song Name" },
                  { title: "Similarity Score" }]
    });
  });
}
