var app = angular.module('myApp', []);

app.controller('pageCtrl', function($scope, $http){
	$scope.user_login = localStorage.getItem('login');
	$scope.logout =  function(){
		window.localStorage.clear;		
		window.location.href = "http://localhost:5000/";
	}
});

app.controller('check_login', function($scope, $http) {

	$scope.login = function() {
		$http.get('http://localhost:5000/api/usuarios/'+$scope.dados.login)
		.then(function(response) {
				if (response.data.password == $scope.dados.password){
					window.localStorage.setItem('login', $scope.dados.login);		
					window.location.href = "http://localhost:5000/home";		
				} else
					alert("Senha invalida");
				
		})
		.catch(function (data) {
			alert("Usuario inválido!");
		});
	}
	$scope.cadastrar = function(){
		$http.post('http://localhost:5000/api/usuarios', $scope.dados).success(function() {
			alert("Usuário cadastrado com sucesso!");
			window.location.href = "http://localhost:5000/";	
		});	
	}

});

app.controller('calendario', function($scope, $http) {
	$http.get('http://localhost:5000/api/usuarios/'+localStorage.getItem('login'))
	.then(function(response) {
		$scope.dados = response.data;
	});
});

app.controller('ctrEventos', function($scope, $http){
	$scope.onclick = false;
	var selectedDescr = '';	
	$http.get('http://localhost:5000/api/usuarios/'+localStorage.getItem('login')+'/eventos')
	.then(function(response) {
		$scope.eventos = response.data.eventos;
	});
	$scope.info = function(ev){
		$scope.dados = ev;
		$scope.onclick = true;
		selectedDescr=$scope.dados.descricao;
	}
	$scope.salvar = function(){
		alert($scope.dados.descricao + '/' + $scope.dados.inicio + '/' + $scope.dados.fim + '/' + $scope.dados.pendente);
		$http.patch('http://localhost:5000/api/usuarios/'+localStorage.getItem('login')+'/eventos/'+ selectedDescr, $scope.dados).success(function() {
			alert("Evento atualizado com sucesso!");
			window.location.href = "http://localhost:5000/calendario";
		});			
	}
	$scope.deletar = function(){
		$http.delete('http://localhost:5000/api/usuarios/'+localStorage.getItem('login')+'/eventos/'+ selectedDescr).success(function() {
			alert("Evento deletado com sucesso!");
			window.location.href = "http://localhost:5000/calendario";
		});			
	}
});

app.controller('cadEventos', function($scope, $http){
	$http.get('http://localhost:5000/api/usuarios')
	.then(function(response) {
		$scope.usuarios = response.data;
	});

	$scope.cadastrar_ev = function(){
		//Adiciono o mesmo evento para o usuario convidado
		envio = $scope.dados;
		envio.pendente = 'true';
		if (typeof($scope.selectedName) != "undefined"){
			$http.post('http://localhost:5000/api/usuarios/'+$scope.selectedName.login+'/eventos', envio).success(function() {
				alert("Convite enviado!");
			});	
		}
		envio.pendente = 'false';
		$http.post('http://localhost:5000/api/usuarios/'+localStorage.getItem('login')+'/eventos', envio).success(function() {
			alert("Evento cadastrado com sucesso!");
			window.location.href = "http://localhost:5000/calendario";	
		});		
	}
});

app.config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('//').endSymbol('//');
    });

