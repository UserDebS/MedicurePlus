import { OrderItem } from "./datatypes"

const apiFetcher = (targetroute : string) => {
    return {
        authByToken : async function() {
            return await fetch(targetroute + 'login', {
                method : 'GET',
                credentials : 'include',
            })
        },
        authByUserPass : async function(email : string, password : string) {
            return await fetch(targetroute + 'login', {
                method : 'POST',
                headers : {
                    'Content-type' : 'application/json'
                },
                credentials : 'include',
                body : JSON.stringify({
                    email : email,
                    password : password
                })
            })
        },
        register : async function(username : string, email : string, password : string) {
            return await fetch((targetroute + 'register'), {
                method : 'POST',
                headers : {
                    'Content-type' : 'application/json'
                },
                credentials : 'include',
                body : JSON.stringify({
                    username : username,
                    email : email,
                    password : password
                })
            })
        },
        getAllMedicines : async function(offset : number, limit : number) {
            return await fetch(targetroute + `medicines/?offset=${offset}&limit=${limit}`, {
                method : 'GET',
                credentials : 'include',
            })
        },
        getMedicineByID : async function(id : number, offset : number, limit : number) {
            return await fetch(targetroute + `medicines/${id}/?offset=${offset}&limit=${limit}`, {
                method : 'GET',
                credentials : 'include',
            })
        },

        getRecommendedListByID : async function(id : number, offset : number, limit : number) {
            return await fetch(targetroute + `recommendation/${id}/?offset=${offset}&limit=${limit}`, {
                method : 'GET',
                credentials : 'include'
            })
        },
        
        getSuggestions : async function(search : string) {
            return await fetch(targetroute + `suggestions/?search=${search}`, {
                method : 'GET',
                credentials : 'include',
            })
        },
        getSearched : async function(search : string, offset : number, limit : number) {
            return await fetch(targetroute + `find/?search=${search}&offset=${offset}&limit=${limit}`, {
                method : 'GET',
                credentials : 'include',
            })
        },
        uploadImage : async function(image : string) {
            return await fetch(targetroute + `upload`, {
                method : 'POST',
                headers : {
                    'Content-type' : 'application/json'
                },
                credentials : 'include',
                body : JSON.stringify({
                    image : image
                })
            })
        },
        addOrder : async function(order_list : OrderItem[]) {
            return await fetch(targetroute + `order`, {
                method : 'POST',
                headers : {
                    'Content-type' : 'application/json'
                },
                credentials : 'include',
                body : JSON.stringify({
                    order_list : order_list
                })
            })
        },
        getOrders : async function(ofst : number, lmt : number) {
            return await fetch(targetroute + `order/?offset=${ofst}&limit=${lmt}`, {
                method : 'GET',
                credentials : 'include',
            })
        },
    }
}

export default apiFetcher('http://127.0.0.1:5500/');