import { useNavigate } from "react-router-dom";
import apiFetcher from "../lib/apiFetcher";
import { useAuth } from "../lib/authContext";
import { useEffect } from "react";
import DeliveryOrderLister from "../components/DeliveryOrderLister";

const DeliveryHome = () => {
    const {deliveryValidated, setDeliveryValidationTrue} = useAuth();
    const navigate = useNavigate();

    const deliveryTokenVerification = async () => {
            try {
                const res = await apiFetcher.authByDeliveryToken();
                if (!res.ok) throw new Error("Token verification failed");
    
                const data = await res.json();
                if (data.status === 200) {
                    setDeliveryValidationTrue();
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
        if(!deliveryValidated) {
            // Check if token is valid
            deliveryTokenVerification();
        }        
    }, [deliveryValidated]);

    return ( 
        <div className="size-full overflow-hidden">
            <DeliveryOrderLister />
        </div>
     );
}
 
export default DeliveryHome;