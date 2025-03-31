import { createContext, useContext, useState } from "react";

const authContext = createContext<{
    shopValidated : boolean;
    setShopValidationTrue : () => void;
    deliveryValidated : boolean;
    setDeliveryValidationTrue : () => void;
} | null>(null);

export const AuthProvider : React.FC<{
    children : React.ReactNode
}> = ({ children }) => {
    const [shopValidated, setShopValidated] = useState<boolean>(false);
    const [deliveryValidated, setDeliveryValidated] = useState<boolean>(false);

    const setShopValidationTrue = () => {
        setShopValidated(true);
    }

    const setDeliveryValidationTrue = () => {
        setDeliveryValidated(true);
    }



    return (
        <authContext.Provider value={{shopValidated, setShopValidationTrue, deliveryValidated, setDeliveryValidationTrue}}>
            {children}
        </authContext.Provider>
    )
}

export const useAuth = () : {
    shopValidated : boolean;
    setShopValidationTrue : () => void;
    deliveryValidated : boolean;
    setDeliveryValidationTrue : () => void;
} => {
    const context = useContext(authContext);
    if(!context) throw new Error('useAuth must be used within AuthProvider')
    return context;
}