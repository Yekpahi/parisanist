$(document).ready(function () {
  $(".ajaxLoader").hide();
  $(".filter-checkbox").on("click", function(e) {
    e.preventDefault();
    var _filterObj={};
    $(".filter-checkbox").each(function (index,ele) {
      var _filterVal = $(this).val();
      var _filterKey = $(this).data("filter");
      _filterObj[_filterKey] = Array.from(document.querySelectorAll("input[data-filter=" + _filterKey + "]:checked")
      ).map(function(el){
        return el.value;
      });
    });

    // Run Ajax

    $.ajax({
        url: "{% url 'filter_data' %}",
        data:_filterObj,
        dataType:'json',
        beforeSend:function(){
            console.log('coucou')
            $(".ajaxLoader").show();
        },
        success:function(res){
            $("#filteredProducts").html(res.data);
            $("ajaxLoader").hide();
        }
    });
  });
});
