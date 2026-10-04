package sample.payment;

import org.springframework.web.bind.annotation.*;

/** Generics and recursive wire shapes deliberately exercise UNKNOWN boundaries. */
@RestController
@RequestMapping("/unknown")
public abstract class UnknownContractsController<T> {
    @GetMapping("/generic")
    public abstract T generic();

    @GetMapping("/recursive")
    public RecursiveView recursive() { return null; }
}
record RecursiveView(String name, RecursiveView next) {}
