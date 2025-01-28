import {  useState } from "react";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { MedicineDetails } from "@/lib/datatypes";
import apiFetcher from "@/lib/apiFetcher";

const TextSearch = ({ 
    callback 
} : { 
    callback : React.Dispatch<React.SetStateAction<MedicineDetails[]>>
}) => {
    const [searchString, setSearchString] = useState<string>("");
    const [searchData, setSearchData] = useState<string[]>([]);

    const handleChange : React.ChangeEventHandler<HTMLInputElement> = async(e) => {
        setSearchString(e.target.value);
        if(e.target.value === "") {
            setSearchData([]);
            return;
        }

        await apiFetcher.getSuggestions(e.target.value).then(async(res) => {
            const data = await res.json();
            setSearchData(data);
        })
        .catch(_ => console.log(_));
    }

    const handleSubmit : React.MouseEventHandler = async(e) => {
        e.preventDefault();
        if(searchString === "") return;
        setSearchData([]);

        await apiFetcher.getSearched(searchString, 0, 20).then(async(res) => {
            const data  = await res.json();
            callback(data);
        })
        .catch(_ => console.log(_));
    }
    
    return ( 
        <div className="h-10 w-[284.097px] relative">
            <Input 
            className="h-full w-3/4 rounded-r-none inline-block"
            onChange={handleChange}
            value={searchString}
            placeholder="Search"/>
            <Button onClick={handleSubmit} className="inline-block h-full w-1/4 rounded-l-none">Search</Button>
            <div className="absolute max-h-40 w-[284.097px] overflow-x-hidden overflow-y-auto mt-1">
                {
                    searchData.map(item => (
                        <div 
                        className="cursor-pointer bg-white hover:bg-slate-200 p-1 text-lg font-semibold capitalize" 
                        onClick={_ => {setSearchString(item); setSearchData([])}} key={item}>
                            {item}
                        </div>)
                    )
                }
            </div>
        </div>
    );
}
 
export default TextSearch;