function cupcakeHtml(cupcake){
    return `
    <div data-cupcake-id=${cupcake.id}>
      <li>
        ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
        <button class="delete-button">X</button>
      </li>
      <img 
            src="${cupcake.image}"
            style="width: 200px;
              height: 200px;
            "
            alt="(no image provided)">
    </div>
  `
}


const BASE_URL = "http://127.0.0.1:5000/api"

/*show all cupcake*/
async function showAllCupcakes(){
    const response = await axios.get("http://127.0.0.1:5000/api/cupcakes")
    for(let cupcake of response.data.cupcakes){
        let newCupcake = $(cupcakeHtml(cupcake));
        $("#cupcakes-list").append(newCupcake)
    }
}

/*delete the cupcake */
$("#cupcakes-list").on("click", ".delete-button", async function (evt) {
  evt.preventDefault();

  let $cupcake = $(evt.target).closest("div");
  let cupcakeId = $cupcake.attr("data-cupcake-id");

  await axios.delete(`http://127.0.0.1:5000/api/cupcakes/${cupcakeId}`);
  $cupcake.remove();
});


$("#new-cupcake-form").on("submit", async function (evt) {
  evt.preventDefault();

  let flavor = $("#form-flavor").val();
  let rating = $("#form-rating").val();
  let size = $("#form-size").val();
  let image = $("#form-image").val();

  const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    rating,
    size,
    image
  });

  let newCupcake = $(cupcakeHtml(newCupcakeResponse.data.cupcake));
  $("#cupcakes-list").append(newCupcake);
  $("#new-cupcake-form").trigger("reset");
});

$(showAllCupcakes)
