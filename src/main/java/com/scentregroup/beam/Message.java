package com.scentregroup.beam;

import com.google.api.services.bigquery.model.TableRow;
import lombok.Builder;
import lombok.EqualsAndHashCode;
import lombok.Getter;

import java.io.Serializable;

@Builder(toBuilder = true)
@EqualsAndHashCode
@Getter
public class Message implements Serializable {
    private static final long serialVersionUID = 1L;
    private String message;
    public static Message fromTableRow(TableRow tableRow) {
        return Message.builder().message(tableRow.get("message").toString()).build();
    }
}
