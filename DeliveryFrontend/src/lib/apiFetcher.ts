import { AuthData, shopOrDeliveryData } from "./datatypes";

const apiFetcher = (targetRoute : string) => {
    return {
        authByShopToken : async function() {
            return await fetch(
                targetRoute + 'shops/login', 
                {
                    method : 'GET',
                    credentials : 'include',
                }
            );
        },

        authByShopId : async function(
            authData : AuthData
        ) {
            return await fetch(
                targetRoute + 'shops/login',
                {
                    method : 'POST',
                    headers : {
                        "Content-Type": "application/json"
                    },
                    credentials : 'include',
                    body : JSON.stringify({
                        'email' : authData.email,
                        'password' : authData.password
                    })
                }
            );
        }, 

        shopRegister : async function(
            shopData : shopOrDeliveryData
        ) {
            return await fetch(
                targetRoute + 'shops/register',
                {
                    method : 'POST',
                    headers : {
                        "Content-Type": "application/json"
                    },
                    credentials : 'include',
                    body : JSON.stringify({
                        authdata : {
                            email : shopData.authdata.email,
                            password : shopData.authdata.password
                        },
                        locationDetails : {
                            latitude : shopData.locationDetails.latitude,
                            longitude : shopData.locationDetails.longitude,
                            district : shopData.locationDetails.district,
                            state : shopData.locationDetails.state,
                            country : shopData.locationDetails.country
                        }
                    })
                }
            );
        },

        authByDeliveryToken : async function() {
            return await fetch(
                targetRoute + 'deliveries/login', 
                {
                    method : 'GET',
                    credentials : 'include',
                }
            );
        },

        authByDeliveryId : async function(
            authData : AuthData
        ) {
            return await fetch(
                targetRoute + 'deliveries/login',
                {
                    method : 'POST',
                    headers : {
                        "Content-Type": "application/json"
                    },
                    credentials : 'include',
                    body : JSON.stringify({
                        'email' : authData.email,
                        'password' : authData.password
                    })
                }
            );
        }, 

        deliveryRegister : async function(
            shopData : shopOrDeliveryData
        ) {
            return await fetch(
                targetRoute + 'deliveries/register',
                {
                    method : 'POST',
                    headers : {
                        "Content-Type": "application/json"
                    },
                    credentials : 'include',
                    body : JSON.stringify({
                        authdata : {
                            email : shopData.authdata.email,
                            password : shopData.authdata.password
                        },
                        locationDetails : {
                            latitude : shopData.locationDetails.latitude,
                            longitude : shopData.locationDetails.longitude,
                            district : shopData.locationDetails.district,
                            state : shopData.locationDetails.state,
                            country : shopData.locationDetails.country
                        }
                    })
                }
            );
        },

        getOrders : async function() {// one time use function, will get 30 the pending orders in one go
            return await fetch(
                targetRoute + 'shops/orders',
                {
                    method : 'GET',
                    credentials : 'include'
                }
            );
        },

        getOrderMedicineData : async function(
            orderId : number
        ) { // This will gradually ged medicines related to an order as orders will be inserted
            return await fetch(
                targetRoute + `shops/orders/${orderId}`,
                {
                    method : 'GET',
                    credentials : 'include'
                }
            );
        },

        acceptOrder : async function(
            orderId : number
        ) { //There will be a section for accepted orders
            return await fetch(
                targetRoute + 'shops/orders/accept',
                {
                    method : 'POST',
                    headers : {
                        "Content-Type": "application/json"
                    },
                    credentials : 'include',
                    body : JSON.stringify({
                        'orderId' : orderId
                    })
                }
            );
        },

        removeOrder : async function(
            orderId : number
        ) { //Accidentally accepted orders can be removed later
            return await fetch(
                targetRoute + 'shops/orders/reject',
                {
                    method : 'POST',
                    headers : {
                        "Content-Type": "application/json"
                    },
                    credentials : 'include',
                    body : JSON.stringify({
                        'orderId' : orderId
                    })
                }
            );
        },

        getAcceptedOrders : async function() {
            return await fetch(
                targetRoute + 'shops/orders/accept',
                {
                    method : 'GET',
                    credentials : 'include'
                }
            );
        }
    }
};

export default apiFetcher('http://127.0.0.1:5500/');