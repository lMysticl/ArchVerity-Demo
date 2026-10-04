package sample.payment;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/wire")
public class WireController {
    @PostMapping(value = "/dto", consumes = "application/json", produces = "application/json")
    public BasicWireDto convert(@RequestBody BasicWireDto request) { return request; }
}
