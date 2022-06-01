$(document).ready(function() {

  var animating = false;
  var cardsCounter = 0;
  
  var decisionVal = 80;
  var pullDeltaX = 0;
  var deg = 0;
  var $card, $cardReject, $cardLike;
  const data = {};
  const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  var len = document.getElementById("length").value;
  var numOfCards = parseInt(len);
  const element = document.getElementById('cards');
  
 

  function pullChange() {
    if(cardsCounter<=numOfCards){
    animating = true;
    deg = pullDeltaX / 10;
    $card.css("transform", "translateX("+ pullDeltaX +"px) rotate("+ deg +"deg)");

    var opacity = pullDeltaX / 100;
    var rejectOpacity = (opacity >= 0) ? 0 : Math.abs(opacity);
    var likeOpacity = (opacity <= 0) ? 0 : opacity;
    $cardReject.css("opacity", rejectOpacity);
    $cardLike.css("opacity", likeOpacity);
    }
  };

  function release() {
    if(cardsCounter<=numOfCards){


    if (pullDeltaX >= decisionVal) {
      $card.addClass("to-right");
      data[cardsCounter] = "True";
    } else if (pullDeltaX <= -decisionVal ) {
      $card.addClass("to-left");
      data[cardsCounter] = "False";
    }

    if (Math.abs(pullDeltaX) >= decisionVal) {
      $card.addClass("inactive");

      setTimeout(function() {
        $card.addClass("below").removeClass("inactive to-left to-right");
        cardsCounter++;
        console.log(cardsCounter);
        console.log(len);
        if (cardsCounter === numOfCards) {
          
              cardsCounter = 0;
              element.style.visibility="hidden";
              $card.addClass("inactive to-left to-right");
              $.ajax({
                headers: {'X-CSRFToken': csrftoken},
                method: "POST",
                url: "/answer_quiz/",
                data: data
              });
              $card.removeClass("inactive to-left to-right");
              element.style.visibility="visible";
              window.location.href = "http://adityanjothir.pythonanywhere.com/answerers_list/";
          $(".demo__card").removeClass("below");
        }
      }, 300);
    }

    if (Math.abs(pullDeltaX) < decisionVal) {
      $card.addClass("reset");
    }

    setTimeout(function() {
      $card.attr("style", "").removeClass("reset")
        .find(".demo__card__choice").attr("style", "");

      pullDeltaX = 0;
      animating = false;
    }, 300);
  }
};

  $(document).on("mousedown touchstart", ".demo__card:not(.inactive)", function(e) {
    if (animating) return;

    $card = $(this);
    $cardReject = $(".demo__card__choice.m--reject", $card);
    $cardLike = $(".demo__card__choice.m--like", $card);
    var startX =  e.pageX || e.originalEvent.touches[0].pageX;

    $(document).on("mousemove touchmove", function(e) {
      var x = e.pageX || e.originalEvent.touches[0].pageX;
      pullDeltaX = (x - startX);
      if (!pullDeltaX) return;
      pullChange();
    });

    $(document).on("mouseup touchend", function() {
      $(document).off("mousemove touchmove mouseup touchend");
      if (!pullDeltaX) return; // prevents from rapid click events
      release();
    });
  });

}
);