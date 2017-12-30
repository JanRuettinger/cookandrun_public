$( document ).ready(function() {
  var item = $('.form-error');

  for (var i = 0; i <= item.length; i++) {
    $(item[i]).prev().css( "border-color", "red" );
    $(item[i]).prev().css( "border-style", "solid" );

  }
})



//   for (var i = 0; i <= item.length; i++) {
//       if  ($(item[i]).text() !=  '()' && $(item[i]).text() !=  '[]') {
//         $(item[i]).show();
//         $(item[i]).prev().css( "border-color", "red" );
//         //do some other stuff here
//       }
//       else {
//         $(item[i]).hide();
//         console.log("If false branch")
//         $(item[i]).prev().css( "border-color", rgb(177, 177, 177) );
//       }
//   }
// })
