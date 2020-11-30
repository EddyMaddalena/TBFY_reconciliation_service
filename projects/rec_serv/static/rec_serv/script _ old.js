step = null

MAX_NUM_ATTEMPTS_ALLOWED = 3
attempts_so_far = 0

function update_progress_bar( percent ){
	$("#dynamic").css("width", Math.floor(percent) + "%").attr("aria-valuenow", Math.floor(percent)).text(Math.floor(percent) + "%");
}

$( document ).ready(function() {

	function was_answered( el ){
		console.log( 'Performing was_answered' )

		company_number = $(el).find('.company-number').val()   
		not_enough_info = $(el).find('.cb_not_confident').prop("checked" )
		worker_confidence = $(el).find('.worker_confidence')
		name = $(worker_confidence).find('input').attr('name') 

		radioValue = $("input[name='" + name + "']:checked"). val();

		console.log( '  > Company no.: ' + company_number )
		console.log( '  > Not enough info: ' + not_enough_info )
		console.log( '  > radioValue: ' + radioValue)

	}

	function check_answers(){

		attempts_so_far++

		if(attempts_so_far >= MAX_NUM_ATTEMPTS_ALLOWED){

			console.log('Task failed')

			$('#carousel').carousel( $('#slide-failure').index() )

		}else{
			passed = true

			$(".company-item").each( function(i,v){

				company_number = $(v).find('.company-number').val()

				if( $(v).attr('g').trim().charAt(0) == '7' ){

					sliced = $(v).attr('g').trim().slice(1)

					if ( company_number != sliced){
						passed = false
					}
				}
			})

			if(passed){
				$('#carousel').carousel( $('#slide-success').index() )
			}else{
				$('#carousel').carousel( $('#slide-revisit').index() )
			}				
		}
	}


	function getSlideByPos( pos ){
		return $($(".carousel-inner").children()[pos])
	}


	$('#carousel').bind('slide.bs.carousel', function (e) {


		slide_from  = getSlideByPos( e.from )
		slide_to    = getSlideByPos( e.to )

		console.log( "Carusel, from " + e.from + ', to ' + e.to)

		current_progress = step * (e.to + 1)

		// update_progress_bar(  current_progress ) 

		if ( slide_from.hasClass('company-item') ){
			console.log("The list is a company")

			// console.log("slide company, was was_answered: " + was_answered(slide_from))
		}

		if ( slide_to.attr("id") == "slide-q-check" ){
			check_answers()

			e.preventDefault()
			e.stopPropagation()
		}else{

			if( slide_to.hasClass('btn-back') ){
				$('#btn-back').removeClass("d-none")
			}else{
				$('#btn-back').addClass("d-none")
			}

			if( slide_to.hasClass('btn-next') ){
				$('#btn-next').removeClass("d-none")
			}else{
				$('#btn-next').addClass("d-none")
			}
		}
		/*  */

	});

	$("form").submit(function(e) {
		// We can remove some empty data from the form before to submit the data to mTurk
	})

	$("#dynamic").css("width", step + "%").attr("aria-valuenow", step)

	$(".cb_not_confident").change(function(){
		pan_answer = $(this).closest('.col-left').find('.pan_answer')
		pan_answer.toggleClass('reduced-opaicty')
		pan_answer.find('input').prop('disabled', function(i, v) { return !v; });
	})


	$(".btn-reset").click( function(){
		pan_answer = $(this).closest('.col-left').find('.pan_answer')
		pan_answer.find('.company-number').val('')
		pan_answer.find('input:radio').prop('checked', false);
	})

	// Enable tooltips
	$('[data-toggle="tooltip"]').tooltip({html:true});

	// console.log
	step =  100 /  (  $(".company-item").length + 3  ) 
	update_progress_bar( step )



	// $('input').keyup(function() {
	// 	current_slide = $('.carousel-item.active')
	// 	was_answered(current_slide)
	// })

	// $('input').change( function(){
	// 	current_slide = $('.carousel-item.active')
	// 	was_answered(current_slide)
	// })

	$("#btn-revisit").click( function(){

		first = $( $('.company-item').first() ) 

		$('#carousel').carousel(first.index())

	})
})




