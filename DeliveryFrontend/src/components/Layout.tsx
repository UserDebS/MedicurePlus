import { Outlet } from "react-router-dom";
import Header from "./Header";
import { Toaster } from "sonner";
import { AuthProvider } from "../lib/authContext";

const Layout = () => {
    console.log(window.location.href);
    return ( 
        <AuthProvider>
            <div className="h-lvh w-lvw">
                <Toaster />
                <Header />
                <main className="h-[calc(100%-3.5em)]">
                    <Outlet />
                </main>
            </div>
        </AuthProvider>
    );
}
 
export default Layout;