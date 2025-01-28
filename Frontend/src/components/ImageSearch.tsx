import { MedicineDetails } from "@/lib/datatypes";
import { Button } from "./ui/button";
import apiFetcher from "@/lib/apiFetcher";

const ImageSearch = ({
    callback
}: {
    callback: React.Dispatch<React.SetStateAction<MedicineDetails[]>>
}) => {

    const handleChange: React.ChangeEventHandler<HTMLInputElement> = async(e) => {
        e.preventDefault();
        const files = e.currentTarget.files as FileList
        if (files?.length) {
            const image = files?.[0];
            const base64str = await toBase64(image).then(res => res as string).catch(_ => '_blank');
            if(base64str === '_blank') return;
            console.log(await apiFetcher.uploadImage(base64str).then(async(res) => {
                const data = await res.json();
                callback(data);
            })
            .catch(_ => console.log(_)));   
        }
    }

    const toBase64 = async (file: File) => {
        return new Promise((resolve, reject) => {
            const filereader = new FileReader()
            filereader.readAsDataURL(file!)
            filereader.onload = () => {
                resolve(filereader.result)
            }
            filereader.onerror = reject;
        })
    }

    return (
        <div className="h-10 w-auto">
            <Button
                className="h-full"
                onClick={_ => document.getElementById("imageInput")?.click()}>
                Image Search
            </Button>
            <input
                onChange={handleChange}
                className="hidden"
                id="imageInput"
                accept=".jpg,.jpeg,.png"
                type="file" />
        </div>
    );
}

export default ImageSearch;