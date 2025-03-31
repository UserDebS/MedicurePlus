import { useEffect } from "react";
import OrderLister from "../components/OrderLister";
import { useAuth } from "../lib/authContext";
import apiFetcher from "../lib/apiFetcher";
import { useNavigate } from "react-router-dom";

const ShopHome = () => {
    const {shopValidated, setShopValidationTrue} = useAuth();
    const navigate = useNavigate();

    const shopTokenVerification = async () => {
        try {
            const res = await apiFetcher.authByShopToken();
            if (!res.ok) throw new Error("Token verification failed");

            const data = await res.json();
            if (data.status === 200) {
                setShopValidationTrue();
                return;
            } else {
                //Navigate to Auth.tsx
                navigate("/");
            }
        } catch (error : any) {
            console.log(error.message);
            //Navigate to Auth.tsx
            navigate("/");
        }
    };

    useEffect(() => {
        // If not verified then just let the user access the page
        if(!shopValidated) {
            // Check if token is valid
            shopTokenVerification();
        }
    }, [shopValidated]);

    return ( 
        <div className="h-full w-full">
            <OrderLister />
        </div>
    );
}
 
export default ShopHome;