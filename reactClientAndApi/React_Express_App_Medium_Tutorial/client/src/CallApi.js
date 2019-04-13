
export function getBp(){
    fetch("http://localhost:9000/read_json",{
        method:'GET'
    })
        .then(res => {return(res)});
};


export function createNewBp(){
    fetch("http://localhost:9000/read_json",{
        method:'PUT'
    })
        .then(res => {return(res)});
};
export default createNewBp;