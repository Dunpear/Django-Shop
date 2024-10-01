// Commenting On Another Comment
const CommentingOnAnotherComment = (parentId) => {
    document.querySelector("input[Name='command.ParentId']").value = parentId;
    document.querySelector(".resultMess").style.display = "block";
}
// Reaplace Paginaiton class
const reaplacePagination = () => {
    document.querySelector(".pagination-container").className = "custom-pagination d-flex justify-content-center";
    document.querySelector("ul.pagination").className = "d-flex pagination-links";
    document.querySelector("li a[rel='next']").className = "has-arrow";
    document.querySelector("li a[rel='prev']").className = "has-arrow";
}