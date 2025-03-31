import { useEffect, useState } from "react";
import ShopRegisterForm from "../components/ShopRegisterForm";

import { AuthType } from "../lib/datatypes";
import { Button } from "../components/ui/button";
import ShopLoginForm from "../components/ShopLoginForm";
import DeliveryRegisterForm from "../components/DeliveryRegisterForm";
import DeliveryLoginForm from "../components/DeliveryLoginForm";
import { useAuth } from "../lib/authContext";
import apiFetcher from "../lib/apiFetcher";
import { useNavigate } from "react-router-dom";

const Auth = () => {
    const [authType, setAuthType] = useState<AuthType>(AuthType.ShopRegister);

    const {shopValidated, deliveryValidated, setShopValidationTrue, setDeliveryValidationTrue} = useAuth();
    const navigate = useNavigate();

    //Token verfication for shop and delivery

    const shopTokenVerification = () => {
        apiFetcher.authByShopToken()
        .then(res => {
            if(res.ok) return res.json();
            else throw new Error("Couldn't check");
        })
        .then(res => {
            if(res.status === 200) {
                setShopValidationTrue();
            }
        })
        .catch(_ => console.log('Token verification failed'));
    }

    const deliveryTokenVerification = () => {
        apiFetcher.authByDeliveryToken()
        .then(res => {
            if(res.ok) return res.json();
            else throw new Error("Couldn't check");
        })
        .then(res => {
            if(res.status === 200) {
                setDeliveryValidationTrue();
            }
        })
        .catch(_ => console.log('Token verification failed'));
    }

    useEffect(() => {
        shopTokenVerification();
        deliveryTokenVerification();
    }, []);

    useEffect(() => {
        if(shopValidated) {
            navigate('/shops/home');
        } else if(deliveryValidated) {
            navigate('/deliveries/home');
        }
    }, [shopValidated, deliveryValidated]);

    return ( 
        <div className="h-full w-full flex justify-center items-center background px-5 overflow-hidden">
            <div className="w-1/2 h-[90%] rounded-l-md shadow-lg bg-green-500 overflow-hidden">
                <div className="h-16 flex justify-center items-center gap-2">
                    <Button
                    onClick={(_) => {
                        setAuthType(AuthType.ShopRegister);
                    }} 
                    className={"box-border w-28 " + (authType === AuthType.ShopRegister? "bg-green-800 hover:bg-green-900" : "")}>Shop register</Button>
                    <Button
                    onClick={(_) => {
                        setAuthType(AuthType.ShopLogin);
                    }} 
                    className={"box-border w-28 " + (authType === AuthType.ShopLogin? "bg-green-800 hover:bg-green-900" : "")}>Shop login</Button>
                    <Button
                    onClick={(_) => {
                        setAuthType(AuthType.DeliveryRegister);
                    }} 
                    className={"box-border w-28 " + (authType === AuthType.DeliveryRegister? "bg-green-800 hover:bg-green-900" : "")}>Delivery register</Button>
                    <Button
                    onClick={(_) => {
                        setAuthType(AuthType.DeliveryLogin);
                    }} 
                    className={"box-border w-28 " + (authType === AuthType.DeliveryLogin? "bg-green-800 hover:bg-green-900" : "")}>Delivery login</Button>
                </div>
                {
                    authType === AuthType.ShopRegister? 
                    <ShopRegisterForm /> :
                    authType === AuthType.ShopLogin?
                    <ShopLoginForm /> :
                    authType === AuthType.DeliveryRegister?
                    <DeliveryRegisterForm /> :
                    <DeliveryLoginForm />
                }
            </div>
            <div className="w-1/2 h-[90%] rounded-r-md shadow-lg relative">
                <h1 className="absolute top-[10%] left-0 text-center w-full capitalize font-extrabold text-5xl text-green-500">We promise, we deliver</h1>
                <img src="Background.png" alt="Background" className="object-cover h-full w-full bg-no-repeat"/>
            </div>
        </div>
     );
}
 
export default Auth;