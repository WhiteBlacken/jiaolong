(function($) {
	"use strict";
	$(function(){
		$( '.sw-portfolio-product' ).each(function(){
			var $this 				= $(this);
			var $id 				= this.id;
			var $pf_id 				= ('#' + this.id );
			var $container_id 		= $('#container_'+ $id);
			var $tab_id 			= $('#tab_'+ $id);
			var $container 			= $container_id; //The ID for the list with all the blog posts
			$container.imagesLoaded().progress( function() {
				$container.isotope({ //Isotope options, 'item' matches the class in the PHP
					layoutMode : 'fitRows'
				});
			});		 
			//Add the class selected to the item that is clicked, and remove from the others
			var $optionSets = $tab_id,
			$optionLinks 	= $optionSets.find('li');
			$optionLinks.on('click', function(){
				var $this 	= $(this);
				var dtlink 	= $this.data('href');
				$('.item-pmore > a').attr( 'href', dtlink );
				// don't proceed if already selected
				if ( $this.hasClass('selected') ) {
				  return false;
				}
				var $optionSet = $this.parents($tab_id);
				$optionSets.find('.selected').removeClass('selected');
				$this.addClass('selected');
			 
				//When an item is clicked, sort the items.
				 var selector = $(this).attr('data-product-filter');
				$container.isotope({ filter: selector });
				return false;
			});
			var $btn_loadmore 	= $(this).find(' .item-pajax > a');
			var $categories 	= $btn_loadmore.data('categories');
			var $max_page 		= $btn_loadmore.data('maxpage');
			var $attributes 	= $btn_loadmore.data('attributes');
			var $number 		= $btn_loadmore.data('number');
			var $orderby 		= $btn_loadmore.data('orderby');
			var $order 			= $btn_loadmore.data('order');
			var $ajax_url		= $btn_loadmore.data('ajaxurl');
			var $page 			= 1;			
			if( $page >= $max_page ){
				$btn_loadmore.parent().addClass( 'btn-loaded' );
			}
			$btn_loadmore.on( 'click',function(){
				if( $page >= $max_page ){
					return false;
				}
				$(this).parent().addClass('btn-loading');
				jQuery.ajax({
					type: "POST",
					url: $ajax_url,
					data: ({
						action 	: "sw_portfolio_product_ajax",
						catid  	: $categories,
						numb   	: $number,
						orderby	: $orderby,
						order 	: $order,
						page 		: $page,
						attributes: $attributes
					}),
					 success: function(data) {		
						var $newItems = $(data);
						if( $newItems.length > 0 ){
							$newItems.imagesLoaded( function(){
								setTimeout(function(){
									$container_id.isotope('reloadItems').isotope("insert",$newItems);
								}, 500);
							});
							$btn_loadmore.parent().removeClass('btn-loading');
							$page = $page + 1;
							if( $newItems.length < $number ){
								$btn_loadmore.parent().addClass( 'btn-loaded' );
							}
							if( $page >= $max_page ){
								$btn_loadmore.parent().addClass( 'btn-loaded' );
							}							
						}else{
							$btn_loadmore.parent().addClass( 'btn-loaded' );
						}
					}
				});
			});
		});
	});
})(jQuery);


