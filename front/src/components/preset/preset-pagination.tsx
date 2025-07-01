import {Pagination, PaginationContent, PaginationItem, PaginationNext, PaginationPrevious} from "../ui/pagination";

interface PresetPaginationProps {
  currentPage: number;
  setCurrentPage: (currentPage: number) => void;
  maxPages: number;
}

const PresetPagination = ({ currentPage, maxPages, setCurrentPage }: PresetPaginationProps) => {
  const isFirstPage = currentPage == 0;
  const isLastPage = currentPage == maxPages;

  return (
    <Pagination>
      <PaginationContent>
        <PaginationItem>
          <PaginationPrevious
            href="#"
            aria-disabled={isFirstPage}
            className={isFirstPage ? "pointer-events-none opacity-50" : ""}
            onClick={() => {
              if (!isFirstPage) setCurrentPage(currentPage - 1)
            }}
          />
        </PaginationItem>
        <PaginationItem>
          <PaginationNext
            href="#"
            aria-disabled={isLastPage}
            className={isLastPage ? "pointer-events-none opacity-50" : ""}
            onClick={() => {
              if (!isLastPage) setCurrentPage(currentPage + 1)
            }}
          />
        </PaginationItem>
      </PaginationContent>
    </Pagination>
  )
};

export default PresetPagination;
