// JS MENU MOBILE
const botaoMenu = document.querySelector(".cabecalho__menu");
const menu = document.querySelector(".menu-lateral");

botaoMenu.addEventListener("click", function (event) {
  event.preventDefault();
  menu.classList.toggle("menu-lateral--ativo");
});

$(function () {
  $.ajaxSetup({
    headers: {
      "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val(),
    },
  });
});

$(function () {
  $(".inlineform").formset({
    prefix: "{{ formset.prefix }}",
    addText: "Adicionar nova alternativa",
    deleteText: "Remover",
  });
});

$("#versao").change(function () {
  data = $.post("/pergunta/get_capitulos", {
    livro: $("#livros :selected").val(),
    versao: $("#versao :selected").val(),
  });

  data.done(function (data) {
    $("#capitulos").children().remove();
    data.forEach(function (item) {
      $("#capitulos").append(
        $("<option></option>")
          .attr("value", item.id)
          .text(item.capitulo),
      );
    });
  });
});

$("#capitulos").change(function () {
  data = $.post("/pergunta/get_versiculos", {
    livro: $("#livros :selected").val(),
    versao: $("#versao :selected").val(),
    capitulo: $("#capitulos :selected").text(),
  });

  data.done(function (data) {
    $("#versiculos").children().remove();
    data.forEach(function (item) {
      $("#versiculos").append(
        $("<option></option>").attr("value", item.id).text(item.versiculo)
      );
    });
  });
});

$("#versiculos").change(function () {
  data = $.post("/pergunta/get_texto_biblico", {
    livro: $("#livros :selected").val(),
    versao: $("#versao :selected").val(),
    capitulo: $("#capitulos :selected").text(),
    versiculo: $("#versiculos :selected").text(),
  });

  data.done(function (data) {
    var data_texto = JSON.stringify(data);
    $("#texto_biblico").text(data_texto);
  });
});

$("#btn_salvar").click(function () {
  if ($("#radio_biblia").is(":checked")) {
    esvaziaEscolhaTextual();
  }
  if ($("#radio_textual").is(":checked")) {
    esvaziaEscolhaBiblica();
  }
});

$("#radio_biblia").change(function () {
  if ($(this).is(":checked")) {
    $("#section_referencia").show();
    $("#section_textual").hide();
  }
});

verificaCamposOutrasReferencias();
function verificaCamposOutrasReferencias() {
  if ($("#id_outras_referencias").val() == "") {
    $("#section_textual").hide();
    $("#section_referencia").show();
    $("#radio_biblia").prop("checked", true);
  } else {
    $("#section_textual").show();
    $("#section_referencia").hide();
    $("#radio_textual").prop("checked", true);
  }
}

$("#radio_textual").change(function () {
  if ($(this).is(":checked")) {
    $("#section_textual").show();
    $("#section_referencia").hide();
  }
});

$("#radio-escolha").change(function () {
  if ($(this).is(":checked")) {
    showRadioEscolha();
    $(".form-check-label").text("Alternativa errada")
    $("input.checkboxinput.form-check-input").prop("checked", false);
    $("input.checkboxinput.form-check-input").attr("disabled", false);
    verificaCamposOutrasReferencias();
  }
});

$("#radio-completa").change(function () {
  if ($(this).is(":checked")) {
    showRadioCompleta();
  }
});

$("#radio-livro-capitulo").change(function () {
  if ($(this).is(":checked")) {
    showRadioLivroCapitulo();
  }
});

$("#radio-simples").change(function () {
  if ($(this).is(":checked")) {
    showRadioSimples();
    $("input.checkboxinput.form-check-input:not(:checked)").attr("disabled", false);
  }
});

// Garante que campos não selecionados não estejam na requisição POST
function esvaziaEscolhaBiblica() {
  $("#livros").text("");
  $("#versao").text("");
  $("#capitulos").text("");
  $("#versiculos").text("");
  $("#texto_biblico").text("");
}

// Garante que campos não selecionados não estejam na requisição POST
function esvaziaEscolhaTextual() {
  $("#id_texto_biblico").val("");
  $("#id_outras_referencias").val("");
}

function showRadioEscolha() {
  $("#section_alternativa").show();
  $("#section_selecao_referencia").show();
  verificaCamposOutrasReferencias();
  $("#versiculos").show();
  $("input.checkboxinput.form-check-input:not(:checked)").attr("disabled", true);
}

function showRadioCompleta() {
  $("#section_alternativa").hide();
  $("#section_selecao_referencia").hide();
  $("#section_referencia").show();
  $("#versiculos").show();
  $("#section_textual").hide();
}

function showRadioLivroCapitulo() {
  $("#section_alternativa").hide();
  $("#section_selecao_referencia").hide();
  $("#section_referencia").show();
  $("#section_textual").hide();
  $("#versiculos").hide();
  $(".parte__referencia").css("margin-top", "32px");
}

function showRadioSimples() {
  $("#section_alternativa").show();
  $("#section_selecao_referencia").show();
  $("#section_referencia").show();
  $("#versiculos").show();
}

$(function() {
  const selected_tipo_resposta = $('input[name="tipo_resposta"]:checked').val();
  if (selected_tipo_resposta == 'MES') {
      showRadioEscolha();
      return;
  }
  if (selected_tipo_resposta == 'RCO') {
      showRadioCompleta();
      return;
  }
  if (selected_tipo_resposta == 'RLC') {
      showRadioLivroCapitulo();
      return;
  }
  if (selected_tipo_resposta == 'RES') {
      showRadioSimples();
      return;
  }
});