$(document).ready(function(){
  load_similar_songs();
});

function load_similar_songs() {
  $.get("/get_similar_songs", function(data, status){
    var dataSet = data.map(function(a) {
      var similarity_score = Math.round(a.similarity * 100) / 100
      return [a.songname, similarity_score];
    });
    console.log('here 3');
    console.log('dataSet: ' + JSON.stringify(dataSet));
    $('#similar_songs_table').DataTable( {
      data: dataSet,
      columns: [  { title: "Song Name" },
                  { title: "Similarity Score" }],
      "order": [[ 1, "desc" ]],
      "language": {
          "lengthMenu": "Show _MENU_ songs",
          "zeroRecords": "No songs to show",
          "info": "Showing _START_ to _END_ of _TOTAL_ songs",
          "infoEmpty":      "No songs",
          "infoFiltered":   "(filtered from _MAX_ songs)"
      }
    });
  });
}
