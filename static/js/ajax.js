$(document).ready(function(){
	$("#search").submit(function(event){event.preventDefault();});
	$("#search").keyup(function(e){

		//var campo = $("#search").length;
		if ((e.which >= 48 && e.which <= 90) && e.which != 8){
			$.ajax({
				url: $(this).attr('action'),
				type: $(this).attr('method'),
				data: $(this).serialize(),

				success: function(json){
					$('#search-result').empty();
					for(var i = 0; i < json.length; i++) {
				   		var obj = json[i];
						$("#search-result").append('<li class="dropdown-item"><a target="_blank" href="leer/'+obj.id+'">'+obj.codigo+'</a></li>')
					}
				}
			})
		}

		if (e.which == 8) {
			$('#search-result').empty();			
		}
	})
})

function searchSuccess(data, textStatus, jqXHR) {
	// body...
	$('#search-result').html(data);
}