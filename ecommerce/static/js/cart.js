//console.log("Hello World")
var updateBtns = document.getElementsByClassName('update-cart')

for (i=0 ; i<updateBtns.length;i++){
    updateBtns[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId :',productId,',Action : ',action)
        console.log('user : ',user)

        if (user == 'AnonymousUser'){
            console.log('User is not signed in..')
        }
        else{
            console.log('User is signed in..')
            updateUserOrder(productId,action)
        }

    })
}

function updateUserOrder(productId,action){
    console.log('Sending Data..')
    //console.log(productId,action,'will be used to update user order')
    //console.log('X-CSRFToken', csrftoken)
    var url = '/update_item/'

    fetch(url,{
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'productId': productId,'action':action}),
    })

    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        console.log('data : ',data)
        location.reload()
    });

}






 

