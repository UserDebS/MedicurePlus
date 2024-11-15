import { useNavigate } from "react-router";
import { Button } from "./button";

const Header = () => {
    const navigate = useNavigate()
    return ( 
        <div className="w-full h-14 shadow-md">
            <div className="size-full flex justify-between items-center px-2">
                <div className="h-full">
                    <img className="h-full object-cover" src="logo.png" alt="logo"/>
                </div>
                <div className="h-full gap-5 flex justify-around items-center px-2">
                    <p className="text-slate-500 text-[17px] font-semibold cursor-pointer" onClick={_ => navigate('/home')}>Home</p>
                    <Button onClick={_ => navigate('/history')}>Order History</Button>
                </div>
            </div>
        </div>
     );
}
 
export default Header;