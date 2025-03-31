import { useEffect, useState } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { toast } from "sonner";
import apiFetcher from "../lib/apiFetcher";
import { useAuth } from "../lib/authContext";

const DeliveryRegisterForm = () => {
    const [email, setEmail] = useState<string>('');
    const [password1, setPassword1] = useState<string>('');
    const [password2, setPassword2] = useState<string>('');
    const [district, setDistrict] = useState<string>('');
    const [state, setState] = useState<string>('');
    const [country, setCountry] = useState<string>('');
    const [latitude, setLatitude] = useState<number | null>(null);
    const [longitude, setLongitude] = useState<number | null>(null);

    const [locationPermission, setLocationPermission] = useState<boolean>(false);
    const {setDeliveryValidationTrue} = useAuth();

    const handleSubmit : React.FormEventHandler<HTMLFormElement> = async(event) => {
        event.preventDefault();

        if(!locationPermission){
            toast(
                <span className="text-red-500 font-bold">
                    Enable location to register!
                </span>
            );
            return;
        }

        if(
            email === '' ||
            password1 === '' ||
            password2 === '' ||
            district === '' ||
            state === '' ||
            country === ''
        ) {
            toast(
                <span className="font-bold text-red-500">
                    Fields are not set properly!
                </span>
            )
            return;
        }

        if(password1 !== password2) {
            toast(
                <span className="font-bold text-red-500">
                    Passwords are not the same!
                </span>
            );
            return;
        }

        if(latitude === null || longitude === null) {
            toast( 
                <span className="font-bold text-red-500">
                    Couldn't read location!
                </span>
            );
            return;
        }

        //Register logic

        await apiFetcher.deliveryRegister({
            authdata : {
                email : email,
                password : password1
            },
            locationDetails : {
                latitude : latitude,
                longitude : longitude,
                district : district,
                state : state,
                country : country
            }
        })
        .then(res => res.json())
        .then(res => {
            if(res.status === 201) {
                toast(
                    <span className="font-bold text-green-500">
                        Account has been created!
                    </span>
                );
                //Navigation will be handled by Auth.tsx
                setDeliveryValidationTrue();
            } else {
                toast(
                    <span className="font-bold text-red-500">
                        Account already exists!
                    </span>
                );
            }
        })
        .catch(_ => {
            toast(
                <span className="font-bold text-red-500">
                    Account already exists!
                </span>
            );
        })
    }

    const setGeolocation = () => {
        window.navigator.geolocation.getCurrentPosition(
            (location) => {
                console.log('Setting location');
                setLatitude(location.coords.latitude);
                setLongitude(location.coords.longitude);
            },
            (err) => {
                toast(
                    <span className="text-red-500 font-bold">
                        Couldn't read location!<br />
                        {err.message}
                    </span>
                );
            }
        );
    };

    const handleLocationPermission = () => {
        if (!("permissions" in navigator)) {
            setGeolocation();
            toast(
                <strong className="text-yellow-800">
                    Looks like you are using browsers like Safari or Firefox etc. <br />
                    If possible switch to <em>Chrome</em> for best experience.
                </strong>
            )
            return;
        }

        window.navigator.permissions
        .query({name : 'geolocation'})
        .then(permissionStatus => {
            setLocationPermission(permissionStatus.state === 'granted');
            if(!(permissionStatus.state === 'granted')) toast(
                <span className="text-red-500 font-bold">
                    Enable location to register!
                </span>
            );
            else {
                setGeolocation();
            }
            permissionStatus.onchange = () => {
                if(permissionStatus.state === 'granted') {
                    setLocationPermission(true);
                    setGeolocation();
                }
                else setLocationPermission(false);   
            }
        })
        .catch(_ => {
            toast(
                <span className="text-red-500 font-bold">
                    Couldn't read permission status!
                </span>
            )
        })
    }

    useEffect(() => {
        handleLocationPermission();
    }, []);

    return (
        <form className="h-full w-full p-2" onSubmit={handleSubmit}>
            <h1 className="font-bold text-4xl text-white">Register as a delivery person</h1>
            <label className="font-bold">
                Email
                <Input
                value={email}
                onChange={(e) => {
                    setEmail(e.target.value);
                }}
                className="w-1/2 bg-white" type="email" required/>
            </label>
            <label className="font-bold">
                Password
                <Input
                value={password1}
                onChange={(e) => {
                    setPassword1(e.target.value);
                }}
                className="w-1/2 bg-white" type="password" required/>
            </label>
            <label className="font-bold">
                Re-type your password
                <Input
                value={password2}
                onChange={(e) => {
                    setPassword2(e.target.value);
                }}
                className="w-1/2 bg-white" type="password" required/>
            </label>
            <label className="font-bold">
                District
                <Input
                value={district}
                onChange={(e) => {
                    setDistrict(e.target.value);
                }}
                className="w-1/2 bg-white" type="text"
                required/>
            </label>
            <label className="font-bold">
                State
                <Input
                value={state}
                onChange={(e) => {
                    setState(e.target.value);
                }}
                className="w-1/2 bg-white" type="text"
                required/>
            </label>
            <label className="font-bold">
                Country
                <Input
                value={country}
                onChange={(e) => {
                    setCountry(e.target.value);
                }}
                className="w-1/2 bg-white" type="text"
                required/>
            </label>
            <br />
            <p className="m-0 p-0 border-0 font-bold text-white"><strong>Already have an account? Go to Delivery Login!</strong></p>
            <br />
            <Button
            disabled={!locationPermission}
            className={locationPermission? "" :
                "bg-red-500"
            }
            type="submit">{
                locationPermission?
                "Register":
                "Grant location permission to register!"
            }</Button>
        </form>
    );
}
 
export default DeliveryRegisterForm;